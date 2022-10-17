from decouple import config
from pip import main
from plugins.error_check_plugin import error_check
from plugins.events_check_plugin import events_check

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"

if __name__ == '__main__':
    error_check(username=username, userpwd=userpwd, dsn=dsn)
    events_check(username=username, userpwd=userpwd, dsn=dsn)