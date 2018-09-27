from typing import List

from bdpf.dao import TargetTableDao as Dao
from bdpf.model.TableInfo import TableInfo
from bdpf.service import CheckAlgorithm, FileRead


def upload_check(file_path):
    # 接收上传的excel文件，获取文件存储的路径。方法返回上传文件的路径。
    # 根据路径解析文件，入参为上传文件的存储路径，返回解析后的list。
    # 获取已上线的表名，返回list。
    # 获取已受理的表名，返回list。
    # 将解析的list进行查重，返回带有查重结果的list。入参两个list，返回一个list。
    table_list: List[TableInfo] = FileRead.read_excel(file_path)
    # 循环对上传的表进行查重
    for t in table_list:
        # 检查来源系统是否存在
        src_count = Dao.select_src_system(t.src_system)
        if src_count > 0:  # 存在
            Dao.select_processed_name(t.src_system)
            received_list = Dao.select_received_name(t.src_system)
            processed_list = Dao.select_processed_name(t.src_system)
            CheckAlgorithm.check_repeat(t, received_list, '已受理')
            CheckAlgorithm.check_repeat(t, processed_list, '已上线')
        else:  # 不存在
            t.result = 3
            t.msg = '来源系统不存在'
    return table_list

