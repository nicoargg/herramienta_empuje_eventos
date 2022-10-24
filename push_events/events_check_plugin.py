from datetime import datetime
import csv


from push_events.extract.extract_sku import extract_sku_list
from push_events.extract.execute_query import execute_query


sku_tuple = extract_sku_list()


events_query= """
SELECT * FROM ultimo_saldo_sku q
WHERE TRIM(sku) IN {sku_tuple}
and q.fecha_modificacion >= To_date('{y_date}','dd-mm-yyyy hh24:mi:ss')
"""

def events_check(dsn, username, userpwd):
    if type(sku_tuple) == str:
        output = execute_query(username=username, dsn=dsn, userpwd=userpwd, query=events_query, sku_tuple=f"('{sku_tuple}')")
    elif type(sku_tuple) == tuple:
        output = execute_query(username=username, dsn=dsn, userpwd=userpwd, query=events_query, sku_tuple=sku_tuple)
    # Nombrado fecha sin puntos para crear un archivo
    if len(output[0]) > 0:
        parsed_date = datetime.today().strftime('%d-%m-%Y %H-%M-%S')
        # Creando archivo csv con los datos de envio de stock
        with open(f"./eventos_enviados/{parsed_date}.csv", "a+", newline='') as f:
            write = csv.writer(f)
            for row in output[0]:
                sku = "".join(row[1].split())
                write.writerow([row[0], sku, row[2], row[3], row[6], row[7]])
            f.close()
        print("archivo de eventos generado")
    else: print("No hay eventos")