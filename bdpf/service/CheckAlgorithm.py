import random

from bdpf.model.TableInfo import TableInfo


def check_repeat(table_info: TableInfo, target_list: list):
    i = random.randint(0, 2)
    table_info.result = i
    print("type is ")
    print(type(target_list))
    return table_info
