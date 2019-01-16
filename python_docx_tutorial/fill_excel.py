import xlrd
import os
import re
from xlutils.copy import copy

excel_file_path = 'excel/课堂测试成绩.xlsx'

# step 1： 复制并且获取第一个sheet
data = xlrd.open_workbook(excel_file_path)
# 拷贝一份原来的excel
book_new = copy(data)
sheet_new = book_new.get_sheet(0)

table = data.sheets()[0]
print(table.nrows)

# step 2： 建立学号与行号的对应，方便后续的操作
dic_stuid_row_num = {}

for i in range(table.nrows):
    if i == 0:
        continue
    text = table.row_values(i)
    dic_stuid_row_num[text[0]] = i

# print(dic_stuid_row_num)

# step 3： 遍历文件，将对应的成绩填入excel
re_num = r"\d+"
pt_num = re.compile(re_num)

files = ['chapter2.txt', 'chapter3.txt', 'chapter4.txt', 'chapter5.txt']
sub_nums = [32, 45, 30, 30]
base_dir = 'files'

for index in range(len(files)):
    path = os.path.join(base_dir, files[index])
    with open(path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:

            rs = pt_num.findall(line)

            print(rs)

            stu_id = rs[0]
            score = int(rs[1]) / sub_nums[index]

            if stu_id in dic_stuid_row_num.keys():
                row_num = dic_stuid_row_num[stu_id]
                sheet_new.write(row_num, index + 3, '%.2f' % (score * 100))


book_new.save('课堂测试成绩.xls')




