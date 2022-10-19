from decouple import config
from push_events.error_check_plugin import error_check
from push_events.events_check_plugin import events_check

username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"

if __name__ == '__main__':
    error_check(username=username, userpwd=userpwd, dsn=dsn)
    events_check(username=username, userpwd=userpwd, dsn=dsn)