#-*- coding:utf-8 -*-
def GenGroup(requirements):
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
    return (list_unmatch, list_match, list_maybe)


