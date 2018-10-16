# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 15:14:56 2018

@author: liub7
"""

from bdpf.dao.ConnectDbUtils import get_mysql_connect
from bdpf.model.DbInfo import DbInfo
from bdpf.model.MetaGenerate import MetaGenerate


# 获取数据库连接
def get_db_conn():
    return get_mysql_connect()


# 查找所有received_state=1的表信息（待生成元数据）
def get_table_info(t_name='', src_system=''):
    conn = get_db_conn()
    cur = conn.cursor()
    received_list = []
    if t_name == '' and src_system == '':
        sql = "select id,t_name,src_system,user_name from received_table where received_state=1"
    else:
        sql = """select id,t_name,src_system,user_name from received_table where received_state=1 and t_name='{}' 
        and src_system='{}'""".format(t_name, src_system)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        for d in data:
            received_list.append(d)
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
        return received_list


# 插入表结构信息
def write_field_info(db_name, src_table_en_name, table_cn_name):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = "SELECT column_name,COLUMN_COMMENT,data_type,COLUMN_KEY from information_schema.COLUMNS " \
          "where TABLE_SCHEMA='" + db_name + "' and TABLE_NAME='" + src_table_en_name + "'"
    print(sql)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        for d in data:
            # received_list.append(d)
            if d[3] == "PRI":
                is_key = "Y"
            else:
                is_key = "N"
            sql = """INSERT INTO ETL_TABLE_FIELD_INFO(src_table_en_name,table_cn_name,field_en_name,field_cn_name,
            field_type,is_primarykey) VALUES ("{}","{}","{}","{}","{}","{}")""".format(src_table_en_name, table_cn_name,
                                                                                       d[0], d[1], d[2], is_key)
            print(sql)
            cur.execute(sql)
            conn.commit()
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
        return len(data)


def generate_meta_data(db_info: DbInfo, conn, meta: MetaGenerate):
    t_id = meta.t_id
    applicant = meta.applicant
    cur = conn.cursor()
    data = query_src_table_info(meta, conn)
    res = 'fail'
    if data:
        tgt_table_en_name = db_info.tgt_table_en_name
        db_name = db_info.db_name
        host_name = db_info.host_name
        user_name = db_info.host_name
        passwd = db_info.passwd

        # 插入表结构信息ETL_TABLE_FIELD_INFO
        src_table_en_name = meta.src_table_en_name
        table_cn_name = meta.table_cn_name
        num_seperator = write_field_info(db_name, src_table_en_name, table_cn_name)
        if num_seperator == 0:
            meta.generate_state = '生成错误，表结构获取失败'
        else:
            # 插入表的元数据ETL_TABLE_PROPERTY_INFO
            sql = """INSERT INTO ETL_TABLE_PROPERTY_INFO(src_table_en_name,tgt_table_en_name,
            table_cn_name,table_comment,src_system_en_name,src_system_cn_name,extract_mode,
            signal_mode,signal_file,load_type,file_name,encode,seperator,load_freq,priority,
            e_condition,num_seperator,db_name,host_name,user_name,pword,applicant) VALUES 
            ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{},"{}",{},"{}","{}","{}","{}",
            "{}")""".format(meta.src_table_en_name, tgt_table_en_name, meta.table_cn_name, meta.table_comment,
                            meta.src_system_en_name, meta.src_system_cn_name, meta.extract_mode,
                            meta.signal_mode, meta.signal_file, meta.load_type, meta.file_name, meta.encode,
                            meta.seperator, meta.load_freq, meta.priority, meta.e_condition, num_seperator, db_name,
                            host_name, user_name, passwd, applicant)
            print(sql)
            cur.execute(sql)

            # 更新已受理表的状态
            sql = "update received_table set received_state=2 where id=" + str(t_id)
            cur.execute(sql)

            res = 'success'
            meta.generate_state = '生成成功'
            conn.commit()
    return res, meta.generate_state


def query_src_table_info(meta: MetaGenerate, conn):
    sql = "select * from src_table where src_table_en_name='" + meta.t_name + "' and src_system_en_name='" + \
          meta.src_system + "'"
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchone()
    if data:
        meta.src_table_en_name = data[1]
        meta.table_cn_name = data[2]
        meta.table_comment = data[3]
        meta.src_system_en_name = data[4]
        meta.src_system_cn_name = data[5]
        meta.extract_mode = data[6]
        meta.signal_mode = data[7]
        meta.signal_file = data[8]
        meta.load_type = data[9]
        meta.file_name = data[10]
        meta.encode = data[11]
        meta.seperator = data[12]
        meta.load_freq = data[13]
        meta.priority = data[14]
        meta.e_condition = data[15]
    return meta
