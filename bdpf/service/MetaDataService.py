import configparser
import os
from typing import List

from bdpf.dao.ConnectDbUtils import get_mysql_connect
from bdpf.dao.ETLProcess import get_table_info, generate_meta_data, query_src_table_info
from bdpf.model.DbInfo import DbInfo
from bdpf.model.MetaGenerate import MetaGenerate
from bdpf.model.ProcessedInfo import ProcessedInfo


def generate_meta(t_name='', src_system=''):
    conn = get_mysql_connect()

    # db_info: DbInfo = get_info(src_table_en_name, src_system_en_name)
    if t_name == '' and src_system == '':
        received_list = get_table_info()
    else:
        received_list = get_table_info(t_name, src_system)

    need_generate_count = len(received_list)
    generate_count = 0

    generate_list = list()
    for item in received_list:
        t_id = item[0]
        t_name = item[1]
        src_system = item[2].rstrip()
        applicant = item[3]
        print("源表:%s 源系统:%s 申请人:%s" % (t_name, src_system, applicant))

        meta = MetaGenerate()
        meta.t_id = t_id
        meta.t_name = t_name
        meta.src_system = src_system
        meta.applicant = applicant
        meta = query_src_table_info(meta, conn)

        db_info: DbInfo = get_info(meta.src_table_en_name, meta.src_system_en_name)
        # meta.generate_state = '未生成'
        res_tag, generate_state = generate_meta_data(db_info, conn, meta)

        meta.generate_state = generate_state
        generate_list.append(meta)
        if res_tag == 'success':
            generate_count += 1
    return need_generate_count, generate_count, generate_list


# 获取来源系统数据库连接信息
def get_info(src_table_en_name, src_system_en_name):
    if src_system_en_name.rstrip() == 'BDPF':
        tgt_table_en_name = src_table_en_name
    else:
        tgt_table_en_name = 'S_' + src_system_en_name + '_' + src_table_en_name
        src_system_en_name = 'TEST'

    cp = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]
    cp.read(path + "/db_info.cfg")

    db_info = DbInfo()
    db_info.tgt_table_en_name = tgt_table_en_name
    db_info.db_name = cp.get(src_system_en_name, "dbname")
    db_info.host_name = cp.get(src_system_en_name, "hostname")
    db_info.user_name = cp.get(src_system_en_name, "username")
    db_info.passwd = cp.get(src_system_en_name, "passwd")
    print("目标表:%s 数据库名称:%s 主机名称:%s 用户:%s 密码:%s" % (
        db_info.tgt_table_en_name, db_info.db_name, db_info.host_name, db_info.user_name, db_info.passwd))
    return db_info


# 查询元数据
def query_table_meta(t_name, src_system):
    return ""


# 拷贝交换需求表模板
def copy_model_excel(excel_path):
    return ""


# 数据分类，插入excel
def pre_fill_excel(t_list: List[ProcessedInfo]):
    # 按照来源系统分类
    t_list.sort()
    src_system = t_list[1].src_system
    src_list = list()
    for t in t_list:
        if t.src_system == src_system:
            src_list.append(t)
        else:
            # 相同的来源系统，进行excel填写
            fill_excel(src_list)

    return ""


# 根据信息填写excel
def fill_excel(t_list: List[ProcessedInfo]):
    file_path = copy_model_excel("")
    print(file_path)
