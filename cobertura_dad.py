from datetime import datetime, timedelta

import oracledb
from decouple import config

# Plugins
from push_events.extract.extract_sku import extract_sku_list


username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"

sku_tuple = extract_sku_list()

update_saldonsr = """begin
     update {saldonsr} s
     set s.ultimo_umbral = -20, s.pendiente_atg = 1
     where sku in {sku_tuple};
     commit;
    end;"""

periodo_query = """SELECT * FROM periodo where estado_periodo = 1"""


ult_umbral = """select * from {tabla_saldo} s where s.sku in {sku_tuple}"""



with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
    ## Se conecta con la base de datos
    cursor = conn.cursor()
    ## Realiza la consulta en catalyst_sku
    tabla_saldo = cursor.execute(periodo_query).fetchall()
    tabla_saldo = tabla_saldo[0][4].lower()
    cursor.execute(update_saldonsr.format(saldonsr=tabla_saldo, sku_tuple=sku_tuple))
    print(tabla_saldo)
    ultimo_umbral = cursor.execute(ult_umbral.format(tabla_saldo=tabla_saldo, sku_tuple=sku_tuple)).fetchall()
    cursor.execute("commit")
    for row in ultimo_umbral:
        print(row[0],row[1], row[15])
    cursor.close()