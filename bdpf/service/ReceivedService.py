from bdpf.dao import TargetTableDao as Dao


def query_received_table():
    received_list = Dao.select_received()
    return received_list
