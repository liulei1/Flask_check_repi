# -*- coding:utf-8 -*-
from typing import List

from similarity.jarowinkler import JaroWinkler

from bdpf.model.RepeatInfo import RepeatInfo
from bdpf.model.TableInfo import TableInfo


# 查重算法-完全匹配
def check_repeat(table_info: TableInfo, target_list: List, target_tag: str) -> TableInfo:
    # 已重复，直接跳出
    if table_info.result == 1:
        return table_info

    # 初始化为不重复
    table_info.result = 0
    table_info.msg = ''
    for t_name in target_list:
        if t_name.lower() == table_info.t_name.lower():
            table_info.result = 1
            table_info.msg = '与' + t_name + '('+target_tag+')完全重复'
            break
    return table_info


# 查重算法-相似度
def check_repeat_similar(table_info: TableInfo, target_list: List, target_tag: str) -> TableInfo:
    # 已重复，直接跳出
    if table_info.result == 1:
        return table_info

    jk = JaroWinkler()
    similar_list: List[RepeatInfo] = list()
    for t_name in target_list:
        similar_point = jk.similarity(t_name, table_info.t_name)
        restore_result(t_name, similar_point, similar_list)
    # 处理查询后的结果
    similar_msg_list = list()
    similar_result = 0
    for repeat_info in similar_list:
        if repeat_info.similar_point > 0.97:
            similar_result = 1
            similar_msg_list.append('与' + repeat_info.t_name + '('+target_tag+')完全重复')
            # 完全重复就不需要在查找疑似重复
            break
        elif repeat_info.similar_point > 0.7:
            similar_result = similar_result if similar_result == 1 else 2
            similar_msg_list.append('与' + repeat_info.t_name + '('+target_tag+')疑似重复')

    table_info.result = similar_result
    table_info.msg = similar_msg_list
    return table_info


def restore_result(t_name, similar_point, similar_list: List[RepeatInfo]):
    similar_size = 3
    # 相似列表未存满，同时相似度大于0。存入相似列表
    if len(similar_list) < similar_size and similar_point > 0:
        similar_list.append(RepeatInfo(t_name, similar_point))
    else:
        for repeat_info in similar_list:
            if similar_point > repeat_info.similar_point:
                repeat_info.similar_point = similar_point
                repeat_info.t_name = t_name
                break
    # print(type(similar_list))


# 结果分类
def table_group(requirements):
    list_match = list()
    list_unmatch = list()
    list_maybe = list()
    for x in requirements:
        if x.result == 0:
            x.result = '通过'
            list_unmatch.append(x)
        elif x.result == 1:
            x.result = '不通过'
            list_match.append(x)
        else:
            x.result = '其他'
            list_match.append(x)
    res = (list_unmatch, list_match, list_maybe)
    return res
