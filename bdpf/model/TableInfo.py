class TableInfo:
    def __init__(self, t_name, t_cname, src_system, result, msg):
        # 英文表名
        self.t_name = t_name
        # 中文表名
        self.t_cname = t_cname
        # 来源系统
        self.src_system = src_system
        # 查重结果
        self.result = result
        # 查重信息
        self.msg = msg

    def __str__(self):
        return 't_name:' + self.t_name + '; result:' + self.result
