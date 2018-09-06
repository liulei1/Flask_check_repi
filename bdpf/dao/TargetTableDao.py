import configparser
import os
from typing import List

import pymysql

# 执行sql，返回查询结果
from bdpf.model.TableInfo import TableInfo


def mysql_connect_select(sql):
    cp = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]
    cp.read(path + "/config.cfg")
    mysql_host = cp.get("MYSQL", "host")
    # print(mysql_host)
    mysql_username = cp.get("MYSQL", "username")
    mysql_passwd = cp.get("MYSQL", "passwd")
    mysql_database = cp.get("MYSQL", "database")
    conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    received_list = []
    for d in data:
        received_list.append(d[0])
    cur.close()
    conn.close()
    return received_list


# 返回已受理表名列表
def select_received_name():
    sql = "select t_name from received_table"
    received_list = mysql_connect_select(sql)
    return received_list


# 返回已上线表名列表
def select_processed_name():
    sql = "select t_name from processed_table"
    received_list = mysql_connect_select(sql)
    return received_list


# def select_received():
#     sql = "select t_name,t_cname,user_name,submit_date,src_system from received_table"
#     cp = configparser.ConfigParser()
#     path = os.path.split(os.path.realpath(__file__))[0]
#     cp.read(path + "/config.cfg")
#     mysql_host = cp.get("MYSQL", "host")
#     mysql_username = cp.get("MYSQL", "username")
#     mysql_passwd = cp.get("MYSQL", "passwd")
#     mysql_database = cp.get("MYSQL", "database")
#     conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
#     cur = conn.cursor()
#     cur.execute(sql)
#     data = cur.fetchall()
#     received_list: List[TableInfo] = list()
#     for d in data:
#         t_name = d[0]
#         t_cname = d[1]
#         user_name = d[2]
#         submit_date = d[3]
#         src_system = d[4]
#         t = TableInfo(t_name, t_cname, src_system, 0, list(), submit_date, user_name)
#         received_list.append(t)
#     cur.close()
#     conn.close()
#     return received_list


def select_received(t_name="", t_cname=""):
    sql = "select t_name,t_cname,user_name,submit_date,src_system from received_table "
    sql_param = "where 1=1"
    if t_name != "":
        sql_param += " and t_name like '%" + t_name + "%'"
    if t_cname != "":
        sql_param += " and t_cname like '%" + t_cname + "%'"
    sql = sql + sql_param + " order by submit_date desc"
    cp = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]
    cp.read(path + "/config.cfg")
    mysql_host = cp.get("MYSQL", "host")
    mysql_username = cp.get("MYSQL", "username")
    mysql_passwd = cp.get("MYSQL", "passwd")
    mysql_database = cp.get("MYSQL", "database")
    conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    received_list: List[TableInfo] = list()
    for d in data:
        t_name = d[0]
        t_cname = d[1]
        user_name = d[2]
        submit_date = d[3]
        src_system = d[4]
        t = TableInfo(t_name, t_cname, src_system, 0, list(), submit_date, user_name)
        received_list.append(t)
    cur.close()
    conn.close()
    return received_list


def execute_sql(sql):
    cp = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]
    cp.read(path + "/config.cfg")
    mysql_host = cp.get("MYSQL", "host")
    mysql_username = cp.get("MYSQL", "username")
    mysql_passwd = cp.get("MYSQL", "passwd")
    mysql_database = cp.get("MYSQL", "database")
    conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
    cur = conn.cursor()
    count = cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return count
