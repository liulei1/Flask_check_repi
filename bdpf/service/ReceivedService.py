import json
import time
from typing import List

from bdpf.dao import TargetTableDao as Dao, TargetTableDao
# def query_received_table():
#     received_list = Dao.select_received()
#     return received_list
from bdpf.service.MetaDataService import generate_meta


def query_received_table(t_name="", t_cname=""):
    received_list = Dao.select_received(t_name, t_cname)
    return received_list


# 存储已受理表信息
def receive_submit(json_list: List, user_name):
    sql_pre = "insert into etl_check.received_table (t_name,t_cname,src_system,submit_date,user_name,received_state) " \
              "values "
    sql_param = ""
    for t_json in json_list:
        print(t_json)
        t_dict = json.loads(t_json)
        t_name = t_dict["t_name"]
        t_cname = t_dict["t_cname"]
        src_system = t_dict["src_system"]

        submit_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # received_state = '0'
        received_state = '1'
        sql_param += "('" + t_name + "','" + t_cname + "','" + src_system + "','" + submit_data + "','"\
                     + user_name + "','" + received_state + "'),"
    sql = sql_pre + sql_param[0:len(sql_param) - 1]
    print(sql)
    TargetTableDao.execute_sql(sql)

    for t_json in json_list:
        t_dict = json.loads(t_json)
        t_name = t_dict["t_name"]
        src_system = t_dict["src_system"]
        print("生成'{}'.'{}'元数据".format(src_system, t_name))
        # 生成元数据
        generate_meta(t_name, src_system)
    return "success"

