import oracledb
from datetime import datetime, timedelta

output= []
## Fecha de hoy - 1 día
t_date = datetime.today()
y_date = t_date + timedelta(days= -1)
y_date = y_date.strftime('%d-%m-%Y %H:%M:%S')

def execute_query(username, userpwd,dsn, query, sku_tuple):
    with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
            cursor = conn.cursor()
            fetch_events = cursor.execute(query.format(sku_tuple=sku_tuple, y_date=y_date)).fetchall()
            output.append(fetch_events)
            cursor.close()
    return output