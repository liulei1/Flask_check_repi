import configparser
import os
from typing import List

import pymysql

# 执行sql，返回查询结果
from bdpf.model.TableInfo import TableInfo


def mysql_connect_select(sql):
    conn = get_mysql_connect()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    received_list = []
    for d in data:
        received_list.append(d[0])
    cur.close()
    conn.close()
    return received_list


# 根据来源系统返回已受理表名列表
def select_received_name(src_system):
    sql = "select distinct t_name from received_table where src_system = '" + src_system + "'"
    received_list = mysql_connect_select(sql)
    return received_list


# 根据来源系统返回已上线表名列表
def select_processed_name(src_system):
    sql = "select distinct t_name from processed_table where src_system = '" + src_system + "'"
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
    # cp = configparser.ConfigParser()
    # path = os.path.split(os.path.realpath(__file__))[0]
    # cp.read(path + "/config.cfg")
    # mysql_host = cp.get("MYSQL", "host")
    # mysql_username = cp.get("MYSQL", "username")
    # mysql_passwd = cp.get("MYSQL", "passwd")
    # mysql_database = cp.get("MYSQL", "database")
    # conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
    conn = get_mysql_connect()
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
    conn = get_mysql_connect()
    cur = conn.cursor()
    cur.execute(sql)
    data: tuple = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data


# 根据来源系统返回已受理表名列表
def select_src_system(src_system):
    sql = "select count(*) from src_system where app_short = '"+src_system+"'"
    print(sql)
    conn = get_mysql_connect()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchone()
    count = data[0]
    conn.commit()
    cur.close()
    conn.close()
    return count


# 获取mysql连接
def get_mysql_connect():
    cp = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]
    cp.read(path + "/config.cfg")
    mysql_host = cp.get("MYSQL", "host")
    # print(mysql_host)
    mysql_username = cp.get("MYSQL", "username")
    mysql_passwd = cp.get("MYSQL", "passwd")
    mysql_database = cp.get("MYSQL", "database")
    conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
    return conn

