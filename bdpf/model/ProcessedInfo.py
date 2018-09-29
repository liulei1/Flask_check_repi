class ProcessedInfo:
    # 英文表名
    t_name = ''
    # 中文表名
    t_cname = ''
    # 来源系统
    src_system = ''
    # 更新标志
    update_tag = '0'
    # 目标系统
    des_system = ''
    # 更新结果
    update_msg = ''

    def __init__(self, t_name, src_system, des_system, update_tag='0', t_cname=''):
        self.t_name = t_name
        self.t_cname = t_cname
        self.src_system = src_system
        self.update_tag = update_tag
        self.des_system = des_system
