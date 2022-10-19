from push_events.stock_and_coverage import insert_skus, stock_coverage
from decouple import config
# Plugins
from push_events.plugins.extract_sku import extract_sku_list


username=config('USER')
userpwd = config('PASS')
host = config('HOST')
port = config('PORT')
service_name = config('SERVICE_NAME')

dsn = f"{host}:{port}/{service_name}"

array_skus = extract_sku_list()

if __name__ == "__main__":
    insert_skus(username=username, userpwd=userpwd, dsn=dsn, array_skus=array_skus)
    stock_coverage(username=username, userpwd=userpwd, dsn=dsn, array_skus=array_skus)
    