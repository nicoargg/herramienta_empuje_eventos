import pathlib

PATH = pathlib.Path(__file__).parent.parent.absolute()


def extract_event_list():
    """From 'sku_list.txt' file, extract per line
    an event in string format"""
    t = []
    with open(f"{PATH}/id_event_list.txt", 'r') as f:
        a = f.readlines()
        for i in a:
            t.append(int("".join(i.split())))
        
    return tuple(t)

