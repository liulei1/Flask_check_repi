import xlrd
from xlrd import XLRDError

from bdpf.model.ProcessedInfo import ProcessedInfo
from bdpf.model.TableInfo import TableInfo


def open_excel(file_path):
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(str(e))


# 解析Excel-用户申请
def read_excel(file_path):
    table_list = []
    try:
        data = open_excel(file_path)
        table = data.sheet_by_name(u'需求申请表')
        nrows = table.nrows
        for rownum in range(2, nrows):
            row = table.row_values(rownum)
            if row:
                t_name = row[3].strip()
                t_cname = row[4].strip()
                src_system = row[2].strip()
                t = TableInfo(t_name, t_cname, src_system, '0', '')
                table_list.append(t)
        return table_list
    except XLRDError:
        return table_list


# 解析Excel-更新已受理
def read_excel_update(file_path):
    table_list = []
    try:
        data = open_excel(file_path)
        table = data.sheet_by_name(u'受理更新表')
        nrows = table.nrows
        for rownum in range(1, nrows):
            row = table.row_values(rownum)
            if row:
                t_name = row[1].strip()
                t_cname = row[2].strip()
                src_system = row[3].strip()
                if t_name != "" and t_cname != "" and src_system != "":
                    # 表名 源系统 目标系统必填
                    t = ProcessedInfo(t_name, t_cname, src_system, 'update')
                else:  # 信息不完整不做更新
                    t = ProcessedInfo(t_name, t_cname, src_system, 'error')
                    t.update_msg = "更新信息不完整"
                table_list.append(t)
        return table_list
    except XLRDError:
        return table_list
