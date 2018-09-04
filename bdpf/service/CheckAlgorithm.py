# -*- coding:utf-8 -*-
import random

from bdpf.model.TableInfo import TableInfo


# 查重算法
def check_repeat(table_info: TableInfo, target_list: list):
    i = random.randint(0, 2)
    table_info.result = i
    print("type is ")
    print(type(target_list))
    return table_info


# 结果分类
def table_group(requirements):
    list_match = list()
    list_unmatch = list()
    list_maybe = list()
    for x in requirements:
        if x.result == 1:
            x.result = '重复'
            list_match.append(x)
        elif x.result == 2:
            x.result = '疑似'
            list_maybe.append(x)
        else:
            x.result = '不重复'
            list_unmatch.append(x)
    res = (list_unmatch, list_match, list_maybe)
    return res
