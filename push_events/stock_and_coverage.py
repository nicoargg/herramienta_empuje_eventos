import oracledb

def insert_skus(username:str, userpwd:str, dsn:str, array_skus):
    catalyst_sku_query = """select * from catalyst_sku where sku in {sku_tuple}"""
    insert_query = """insert into catalyst_sku (SKU, FECHA_ACT, ACTIVO) values ({sku}, to_date('16-05-2022 00:01:00', 'dd-mm-yyyy hh24:mi:ss'),0)"""


    # Si la cantidad de skus es mayor a 990, array_skus será lista
    # Si es menor a 990, será tupla
    # si es un solo sku, será una cadena (texto)
    array_skus = array_skus

    with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
        ## Se conecta con la base de datos
        cursor = conn.cursor()
    # Lista, más de 990 skus
        if type(array_skus) == list:
            for sku_tuple in array_skus:
                sku_in_cata = []
                ## Realiza la consulta en catalyst_sku
                res = cursor.execute(catalyst_sku_query.format(sku_tuple=sku_tuple)).fetchall()
                
                for row in res:
                    sku_in_cata.append("".join(row[0].split()))
                
                print('skus in table catalyst_sku: ',len(sku_in_cata))
                print('skus in sku_list.txt: ',len(sku_tuple))
                if len(sku_in_cata) < len(sku_tuple):
                    contador = 0
                    for sku in sku_tuple:
                        if not sku in sku_in_cata:
                            contador +=1
                            cursor.execute(insert_query.format(sku=sku))
                    cursor.execute("commit")
                    print("se insertaron " + str(contador) + " skus")
    # Tupla, menos de 990 skus pero mas que 1        
        elif type(array_skus) == tuple:
            sku_in_cata = []
            ## Realiza la consulta en catalyst_sku
            res = cursor.execute(catalyst_sku_query.format(sku_tuple=array_skus)).fetchall()
            for row in res:
                sku_in_cata.append("".join(row[0].split()))
            
            ## Si no estan todos los sku, se insertan en la tabla
            # se verifica comparando la cantidad de filas de la tabla 
            # con el la cantidad de skus en la tupla
            print('skus in table catalyst_sku: ',len(sku_in_cata))
            print('skus in sku_list.txt: ',len(array_skus))
            if len(sku_in_cata) < len(array_skus):
                print('Faltan skus en catalyst')
                contador = 0
                for sku in array_skus:
                    if not sku in sku_in_cata:
                        contador +=1
                        cursor.execute(insert_query.format(sku=f"'{sku}'"))
                cursor.execute("commit")
                print("se insertaron " + str(contador) + " skus")
        # String, un sku
        elif type(array_skus) == str:
            res = cursor.execute(catalyst_sku_query.format(sku_tuple=f"('{array_skus}')")).fetchall()
            if len(res) == 0:
                cursor.execute(insert_query.format(sku=f"'{array_skus}'"))
                cursor.execute("commit")
                print("se insertó el sku: " + array_skus)
        cursor.close()





def stock_coverage(username:str, userpwd:str, dsn:str, array_skus):
    ## Revisar tipostock y cod proveedor
    producto_query = """select SKU, TIPOSTOCK, CODIGOPROVEEDORPPAL from producto where SKU IN"""
    ## Enviar cobertura
    cobertura_query = """BEGIN prc_resend_config_ctlyst({cp}, {sku}, NULL); END;"""
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
    # Si la cantidad de skus es mayor a 990, array_skus será lista
    # Si es menor a 990, será tupla
    # si es un solo sku, será una cadena (texto)
    array_skus = array_skus

    with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
        ## Se conecta con la base de datos
        cursor = conn.cursor()

        # Lista, Más de 990 skus
        if type(array_skus) == list:
            for sku_tuple in array_skus:
                print(len(sku_tuple))

                producto = cursor.execute(f"{producto_query} {sku_tuple}").fetchall()
                
                for row in range(len(producto)):
                    ### Si tipostock = S (de la tabla producto)
                    # ejecuta:
                    if (producto[row][1]) == 'S':
                        sku = "".join(producto[row][0].split())
                        cursor.execute(cobertura_query.format(cp="Null", sku=f"'{sku}'"))
                        print(f'{sku}: {producto[row][1]}')
                        cursor.execute("commit")
                    
                    ### Si tipostock = P (de la tabla producto) CC = Codprovvedorppal (prod[row][2])
                    elif (producto[row][1]) == 'P':
                        ccppal = "".join(producto[row][2].split())
                        sku = "".join(producto[row][0].split())
                        cursor.execute(cobertura_query.format(cp=ccppal, sku=f"'{sku}'"))
                        print(f'{sku}: {producto[row][1]}, {ccppal}')
                        cursor.execute("commit")
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

        # Tupla, menos de 990 skus pero mas que 1        
        elif type(array_skus) == tuple:
            ## query para obtener cod_producto, tipo_stock y sku
            producto = cursor.execute(f"{producto_query} {array_skus}").fetchall()
            # Envio de cobertura
            for row in range(len(producto)):
                ### Si tipostock = S (de la tabla producto)
                # ejecuta:
                if (producto[row][1]) == 'S':
                    sku = "".join(producto[row][0].split())
                    cursor.execute(cobertura_query.format(cp="Null", sku=f"'{sku}'"))
                    print(f'{sku}: {producto[row][1]}')
                    cursor.execute("commit")
                
                ### Si tipostock = P (de la tabla producto) CC = Codprovvedorppal (prod[row][2])
                elif (producto[row][1]) == 'P':
                    ccppal = "".join(producto[row][2].split())
                    sku = "".join(producto[row][0].split())
                    cursor.execute(cobertura_query.format(cp=ccppal, sku=f"'{sku}'"))
                    print(f'{sku}: {producto[row][1]}, {ccppal}')
                    cursor.execute("commit")
            
            ## auditar stock
            ## Obtenemos que tabla está activa
            # (saldonsr_a o saldonsr_b)
            periodo = cursor.execute(periodo_query).fetchall()
            tabla_saldo = periodo[0][4].lower()
            print(tabla_saldo)
            # auditamos el stock
            cursor.execute(saldo_menos.format(saldonsr=tabla_saldo, sku_tuple=array_skus))
            cursor.execute(saldo_mas.format(saldonsr=tabla_saldo, sku_tuple=array_skus))
            # confirmamos cambios
            cursor.execute("commit")
        # String, un sku
        elif type(array_skus) == str:
            producto = cursor.execute(f"{producto_query} ('{array_skus}')").fetchall()
            ### Si tipostock = S (de la tabla producto)
            if (producto[0][1]) == 'S':
                sku = "".join(producto[0][0].split())
                cursor.execute(cobertura_query.format(cp="Null", sku=f"'{sku}'"))
                print(f'{sku}: {producto[0][1]}')
                cursor.execute("commit")
            
            ### Si tipostock = P (de la tabla producto) CC = Codprovvedorppal (prod[0][2])
            elif (producto[0][1]) == 'P':
                ccppal = "".join(producto[0][2].split())
                sku = "".join(producto[0][0].split())
                cursor.execute(cobertura_query.format(cp=ccppal, sku=f"'{sku}'"))
                print(f'{sku}: {producto[0][1]}, {ccppal}')
                cursor.execute("commit")
            # Extraemos la tabla actual    
            periodo = cursor.execute(periodo_query).fetchall()
            tabla_saldo = periodo[0][4].lower()
            print(tabla_saldo)
            cursor.execute(saldo_menos.format(saldonsr=tabla_saldo, sku_tuple=f"('{array_skus}')"))
            cursor.execute(saldo_mas.format(saldonsr=tabla_saldo, sku_tuple=f"('{array_skus}')"))
            cursor.execute("commit")

        cursor.close()