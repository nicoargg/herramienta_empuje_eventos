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
    sku_list = set(sku_list)
    sku_list = tuple(sku_list)
    if len(sku_list) >= 910:
        output=[sku_list[i:i + 910] for i in range(0, len(sku_list), 910)]
        return output
    elif len(sku_list) == 1:
        return sku_list[0]
    else: return sku_list