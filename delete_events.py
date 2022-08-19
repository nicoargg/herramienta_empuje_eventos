import oracledb
from plugins.extract_event_list import extract_event_list
from decouple import config

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')
dsn = f"{host}:{port}/{service_name}"


borrar_events = "delete from ultimo_saldo_sku where id_ultimo_saldo_sku in"

### extrae los skus del archivo sku_list.txt
events_id = extract_event_list()
mitad_eventos = len(events_id)//2

with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
    cursor = conn.cursor()
    first = cursor.execute(f"{borrar_events} {events_id[mitad_eventos:]}")
    sec = cursor.execute(f"{borrar_events} {events_id[:mitad_eventos]}")
    cursor.execute("commit")
    cursor.close()
