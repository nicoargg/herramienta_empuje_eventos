import oracledb
from plugins.extract_sku import extract_sku_list
from decouple import config

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"

sku_tuple = extract_sku_list()

## revisar si están los sku
catalyst_sku_query = """select * from catalyst_sku where sku in"""
## Insertar los que no están (sku)
insert_query = """insert into catalyst_sku (SKU, FECHA_ACT, ACTIVO) values (:sku, to_date('16-05-2022 00:01:00', 'dd-mm-yyyy hh24:mi:ss'),0)"""
## Revisar tipostock y cod proveedor
producto_query = """select SKU, TIPOSTOCK, CODIGOPROVEEDORPPAL from producto where SKU IN"""
## Enviar cobertura
cobertura_query = """BEGIN prc_resend_config_ctlyst(:cp, :sku, NULL); END;"""
## revisar tabla activa
periodo_query = """SELECT * FROM periodo where estado_periodo = 1"""
## restar 1 saldonsr
saldo_menos = """begin
 update {saldonsr} set saldonsr = saldonsr - 1
 where sku in {sku_tuple};
 commit;
end;"""
## sumar 1 saldonsr
saldo_mas= """begin 
 update {saldonsr} set saldonsr = saldonsr + 1
 where sku in {sku_tuple};
 commit;
end;"""

### extrae los skus del archivo sku_list.txt
sku_in_cata= []

with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
    ## Se conecta con la base de datos
    cursor = conn.cursor()
    ## Realiza la consulta en catalyst_sku
    res = cursor.execute(f"{catalyst_sku_query} {sku_tuple}").fetchall()
    
    ## revisamos que esten todos los sku
    for row in res:
        sku_in_cata.append("".join(row[0].split()))
    
    ## Si no estan todos los sku, se insertan en la tabla
    # se verifica comparando la cantidad de filas de la tabla 
    # con el la cantidad de skus en la tupla
    if len(sku_in_cata) < len(sku_tuple):
        for sku in sku_tuple:
            if not sku in sku_in_cata:
                cursor.execute(insert_query, {"sku":f'{sku}'})
        cursor.execute("commit")
    
    # Una vez se insertan, se vuelve a verificar
    res2 = cursor.execute(f"{catalyst_sku_query} {sku_tuple}").fetchall()
    
    if len(res2) == len(sku_tuple):
        ## query para obtener cod_producto, tipo_stock y sku
        prods = cursor.execute(f"{producto_query} {sku_tuple}").fetchall()
        # Envio de cobertura
        for row in range(len(prods)):
            ### Si tipostock = S (de la tabla producto)
            # ejecuta:
            if (prods[row][1]) == 'S':
                sku = "".join(prods[row][0].split())
                cursor.execute(cobertura_query, cp=None, sku=f'{sku}')
            
            ### Si tipostock = P (de la tabla producto) CC = Codprovvedorppal (prod[row][2])
            elif (prods[row][1]) == 'P':
                ccppal = "".join(prods[row][2].split())
                sku = "".join(prods[row][0].split())
                cursor.execute(cobertura_query, cp=ccppal, sku=f'{sku}')
        
        
        ## auditar stock
        ## Obtenemos que tabla está activa
        # (saldonsr_a o saldonsr_b)
        periodo = cursor.execute(periodo_query).fetchall()
        tabla_saldo = periodo[0][4].lower()
        print(tabla_saldo)
        # auditamos el stock
        cursor.execute(saldo_menos.format(saldonsr=tabla_saldo, sku_tuple=sku_tuple))
        cursor.execute(saldo_mas.format(saldonsr=tabla_saldo, sku_tuple=sku_tuple))
        # confirmamos cambios
        cursor.execute("commit")
    else:
        print("No se insertaron todos los sku en la tabla catalyst_sku")
    

    
    # Cerramos la conexion
    cursor.close()

# para saber que finalizó
print(len(sku_tuple), 'fin')
