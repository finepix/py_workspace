# 计算正确的答案个数（需事先给出答案）
import os
import re
from python_docx_tutorial.ans_extractor import extract
from python_docx_tutorial.score_counter import sc_count


if __name__ == '__main__':
    result = {}
    marked_file = []

    # 章节
    # 第五章
    # true_answers = [1, 4, 4, 2, 3, 2, 4, 3, 4, 4,
    #                 2, 3, 3, 4, 3, 3, 1, 1, 3, 4,
    #                 3, 3, 3, 2, 2, 1, 4, 3, 4, 4]
    # base_dir = 'C:\\Users\\lenovo02\\Documents\\WeChat Files\\Zipcoder\\Files\\第五章\\学生提交'
    # sub_num = 30

    # 第四章
    # true_answers = [2, 1, 4, 2, 4, 1, 4, 2, 1, 4,
    #                 1, 2, 2, 1, 3, 1, 3, 4, 4, 4,
    #                 1, 3, 1, 2, 3, 4, 2, 3, 3, 2]
    # base_dir = 'G:\\test\\课堂测试\\第四章\\课堂测试-学生提交'
    # sub_num = 30

    # 第三章
    true_answers = []
    base_dir = 'G:\\test\\课堂测试'
    sub_num = 45


    # 正则表达式初始化
    regu_stu_id = r"[0-9]"
    pt_stu_id = re.compile(regu_stu_id)

    sec_dirs_files = os.listdir(base_dir)
    for filename in sec_dirs_files:
        pathname = os.path.join(base_dir, filename)
        if os.path.isdir(pathname):
            # true file name
            file_name = os.listdir(pathname)[0]
            file_path = os.path.join(pathname, file_name)
            # print(file_path.title())

            stu_id = pt_stu_id.findall(file_name)
            stu_id = ''.join(stu_id)
            with open(file_path, 'rb') as f:
                [answers, marked] = extract(f, sub_num)
                # assert for the num
                # if len(answers) != sub_num:
                #     print('not correctly detect the subject num! answers number {}'.format(len(answers)))

                if marked:
                    marked_file.append(file_path)
                    continue
                if len(answers) <= sub_num - 10:
                    print('有答案题目少于给定阈值，为{}!'.format(len(answers)))

                # count the score
                score = sc_count(true_answers, answers)
                print('学号：{}，成绩：{}'.format(stu_id, score))
                result[stu_id] = score                          # can be score / sub_num

        else:
            file_path = os.path.join(base_dir, filename)
            stu_id = pt_stu_id.findall(filename)
            stu_id = ''.join(stu_id)
            with open(file_path, 'rb') as f:
                [answers, marked] = extract(f, sub_num)
                # assert for the num
                # if len(answers) != sub_num:
                #     print('not correctly detect the subject num! answers number {}'.format(len(answers)))

                if marked:
                    marked_file.append(file_path)
                if len(answers) <= sub_num - 10:
                    print('有答案题目少于给定阈值，为{}!'.format(len(answers)))

                # count the score
                score = sc_count(true_answers, answers)
                print('学号：{}，成绩：{}'.format(stu_id, score))
                result[stu_id] = score  # can be score / sub_num

    rs_index = sorted(result.keys())
    print('有成绩的人数：{}'.format(len(result)))
    print(result)
    for r in rs_index:
        print('学号：{}， 成绩：{}'.format(r, result[r]))
    print('标注文档数目：{}'.format(len(marked_file)))
    for f in marked_file:
        print(f)

