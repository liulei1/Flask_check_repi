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
    Dao.select_received_name()
    table_list: List[TableInfo] = FileRead.read_excel(file_path)
    target_list = Dao.select_received_name()
    for t in table_list:
        CheckAlgorithm.check_repeat(t, target_list, '已受理')
    return table_list

