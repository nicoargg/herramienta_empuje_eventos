import oracledb
from plugins.extract_sku import extract_sku_list
from decouple import config

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')
dsn = f"{host}:{port}/{service_name}"




id_events = """select q. *, s.eventid FROM ultimo_saldo_sku q, stg_evento_sl_catalyst s
WHERE q.id_stg_evnt_sl_ctlyst = s.id_stg_evnt_sl_ctlyst AND
TRIM(q.sku) IN"""

borrar_events = "delete from ultimo_saldo_sku where id_ultimo_saldo_sku in {sku}"

### extrae los skus del archivo sku_list.txt
sku_tuple = extract_sku_list()
events_list = []
with oracledb.connect(user=username, password=userpwd, dsn=dsn) as conn:
    cursor = conn.cursor()
    res = cursor.execute(f"{id_events} {sku_tuple}").fetchall()
    if len(res) > 0:
        for line in res:
            events_list.append(line[0])
        
        events_tuple = tuple(events_list)
    
        cursor.execute(borrar_events.format(sku=events_tuple))
        cursor.execute("commit")
        print("Eventos Eliminados")
        #res = cursor.execute(f"{id_events} {sku_tuple}").fetchall()
        # first = cursor.execute(f"{borrar_events} {events_id[mitad_eventos:]}")
        # sec = cursor.execute(f"{borrar_events} {events_id[:mitad_eventos]}")
        # cursor.execute("commit")
        cursor.close()
    else:
        print("No existen enventos")
        cursor.close
