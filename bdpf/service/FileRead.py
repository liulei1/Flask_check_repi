import xlrd
from xlrd import XLRDError

from bdpf.model.TableInfo import TableInfo


def open_excel(file_path):
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(str(e))


# 解析Excel
def read_excel(file_path):
    table_list = []
    try:
        data = open_excel(file_path)
        table = data.sheet_by_name(u'需求申请表1')
        nrows = table.nrows
        for rownum in range(2, nrows):
            row = table.row_values(rownum)
            if row:
                t = TableInfo(row[3], row[4], row[2], '0', '')
                table_list.append(t)
        return table_list
    except XLRDError:
        return table_list
