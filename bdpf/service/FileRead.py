import xlrd

from bdpf.model.TableInfo import TableInfo


def open_excel(file_path):
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(str(e))


# 解析Excel
def read_excel(file_path):
    data = open_excel(file_path)
    table = data.sheet_by_name(u'Sheet1')
    nrows = table.nrows
    table_list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            t = TableInfo(row[0], row[1], row[2], '0', '')
            table_list.append(t)
    return table_list
