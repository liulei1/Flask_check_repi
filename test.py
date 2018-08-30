from bdpf.model.TableInfo import TableInfo


def test():
    t1 = TableInfo('table1', '表1', '洞察分析', '0', '')
    t2 = TableInfo('table2', '表2', '洞察分析', '0', '')
    t3 = TableInfo('table3', '表3', '洞察分析', '0', '')
    arr = (t1, t2, t3)
    for t in arr:
        print(t.t_cname)

test()