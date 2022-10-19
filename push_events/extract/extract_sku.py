import pathlib

PATH = pathlib.Path(__file__).parent.parent.parent.absolute()


def extract_sku_list():
    """From 'sku_list.txt' file, extract per line
    an sku in string format"""
    sku_list = []
    with open (f"{PATH}/sku_list.txt",'r') as f:
        lines = f.readlines()
        for line in lines:

            sku_list.append(''.join(line.split()))

    return tuple(sku_list)