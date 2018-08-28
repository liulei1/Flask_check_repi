class TableInfo:
    def __init__(self, t_name, t_cname, prj, result, msg):
        self.t_name = t_name
        self.t_cname = t_cname
        self.prj = prj
        self.result = result
        self.msg = msg

    def __str__(self):
        return 't_name:' + self.t_name + '; result:' + self.result
