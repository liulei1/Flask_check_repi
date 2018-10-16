
import configparser
import os

import pymysql


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

