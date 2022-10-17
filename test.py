from decouple import config
from plugins.events_check_plugin import events_check

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"


events_check(username=username, userpwd=userpwd, dsn=dsn)