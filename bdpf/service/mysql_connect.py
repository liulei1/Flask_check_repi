import pymysql
import  configparser
class Mysql_connect:
    def __init__(self):
        pass
    def mysql_connect_select(self,sql):
        cp = configparser.ConfigParser()
        cp.read("../../config/config.cfg")
        mysql_host = cp.get("MYSQL", "host")
        print(mysql_host)
        mysql_username = cp.get("MYSQL", "username")
        mysql_passwd = cp.get("MYSQL", "passwd")
        mysql_database = cp.get("MYSQL", "database")
        conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
        cur = conn.cursor()
        #    sql = "select * from table"
        cur.execute(sql)
        data = cur.fetchall()
        received_list = []
        for d in data:
            received_list.append(d)
        return received_list
        cur.close()
        conn.close()

    def mysql_connect_select(self,sql="select t_name from received_table"):
        cp = configparser.ConfigParser()
        cp.read("../../config/config.cfg")
        mysql_host = cp.get("MYSQL", "host")
        print(mysql_host)
        mysql_username = cp.get("MYSQL", "username")
        mysql_passwd = cp.get("MYSQL", "passwd")
        mysql_database = cp.get("MYSQL", "database")
        conn = pymysql.connect(mysql_host, mysql_username, mysql_passwd, mysql_database)
        cur = conn.cursor()
        print(sql)
        #    sql = "select * from table"
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        received_list = []
        for d in data:
            received_list.append(d)
        return received_list
        print(received_list)
        cur.close()
        conn.close()

mysql_connect = Mysql_connect()

if __name__ == '__main__':
    mysql_connect.mysql_connect_select()

#def mysql_conect_select(self,sql):
