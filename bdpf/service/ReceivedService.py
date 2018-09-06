import json
import time
from typing import List

from bdpf.dao import TargetTableDao as Dao, TargetTableDao


# def query_received_table():
#     received_list = Dao.select_received()
#     return received_list


def query_received_table(t_name="", t_cname=""):
    received_list = Dao.select_received(t_name, t_cname)
    return received_list


def receive_submit(json_list: List):
    sql_pre = "insert into etl_check.received_table (t_name,t_cname,src_system,submit_date) values "
    sql_param = ""
    for t_json in json_list:
        print(t_json)
        t_dict = json.loads(t_json)
        t_name = t_dict["t_name"]
        t_cname = t_dict["t_cname"]
        src_system = t_dict["src_system"]
        submit_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_param += "('" + t_name + "','" + t_cname + "','" + src_system + "','" + submit_data + "'),"
    sql = sql_pre + sql_param[0:len(sql_param) - 1]
    count = TargetTableDao.execute_sql(sql)
    if count > 0:
        return "success"
    else:
        return "submit nothing"
