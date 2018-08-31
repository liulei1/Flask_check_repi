from bdpf.model.TableInfo import TableInfo
from bdpf.service import CheckAlgorithm


def upload_check(path):
    # 接收上传的excel文件，获取文件存储的路径。方法返回上传文件的路径。
    # 根据路径解析文件，入参为上传文件的存储路径，返回解析后的list。
    # 获取已上线的表名，返回list。
    # 获取已受理的表名，返回list。
    # 将解析的list进行查重，返回带有查重结果的list。入参两个list，返回一个list。

    print(path)
    t1 = TableInfo('test_table1', '表1', '洞察分析', '0', '')
    t2 = TableInfo('test_table2', '表1', '洞察分析', '0', '')
    t3 = TableInfo('test_table3', '表1', '洞察分析', '0', '')
    t11 = TableInfo('test_table11', '表1', '洞察分析', '0', '')
    t22 = TableInfo('test_table22', '表1', '洞察分析', '0', '')
    t33 = TableInfo('test_table33', '表1', '洞察分析', '0', '')
    target_list = ['aaa', 'bbb']
    table1 = CheckAlgorithm.check_repeat(t1, target_list)
    table2 = CheckAlgorithm.check_repeat(t2, target_list)
    table3 = CheckAlgorithm.check_repeat(t3, target_list)
    table11 = CheckAlgorithm.check_repeat(t11, target_list)
    table22 = CheckAlgorithm.check_repeat(t22, target_list)
    table33 = CheckAlgorithm.check_repeat(t33, target_list)
    res_list = [table1, table2, table3, table11, table22, table33]
    return res_list

