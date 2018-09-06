from typing import List


class TableInfo:
    # 英文表名
    t_name = ''
    # 中文表名
    t_cname = ''
    # 来源系统
    src_system = ''
    # 查重结果（整型）0:不重复;1:重复;2:疑似重复
    result = 0
    # 查重信息
    msg: List[str] = list()
    # 提交日期yyyy-MM-dd HH:mm:ss
    submit_date = ''
    # 申请人
    user_name = ''

    # def __init__(self, t_name, t_cname, src_system, result, msg: List[str]):
    #     self.t_name = t_name
    #     self.t_cname = t_cname
    #     self.src_system = src_system
    #     self.result = result
    #     self.msg = msg

    def __init__(self, t_name, t_cname, src_system, result=0, msg: List[str]=list(), submit_date='', user_name=''):
        self.t_name = t_name
        self.t_cname = t_cname
        self.src_system = src_system
        self.result = result
        self.msg = msg
        self.submit_date = submit_date
        self.user_name = user_name

    def __str__(self):
        return 't_name:' + self.t_name + '; result:' + self.result
