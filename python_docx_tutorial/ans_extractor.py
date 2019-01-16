from docx import Document
import re


def ch2num(ch):
    """
            转化为对应的数字，方便后续计算
    :param ch:
    :return:
    """
    dic = {'A': 1, 'B': 2,  'C': 3, 'D': 4}

    return dic[ch]


def extract(f, total_sub):
    """

    :param f:       文件（已打开文件）
    :param total_sub: 总共的题目数量
    :return:
    """
    # save ans for every one
    answers = []
    is_mark = False

    # step 1: init re lib
    regu_sub = r"第\d+题"
    regu_num = r"\d+"
    regu_lin_ans_lin = r"_[A-D]"
    regu_ans = '[A-D]'

    pt_l_a_l = re.compile(regu_lin_ans_lin)
    pt_a = re.compile(regu_ans)
    pt_sub = re.compile(regu_sub)
    pt_sub_num = re.compile(regu_num)

    # step 2: search the doc for answers like a b c d
    print('开始读取文档：{}'.format(f.name))
    doc = Document(f)
    index = 0
    is_find_sub = False
    is_find_ans = False
    sub_num = 1
    for para in doc.paragraphs:

        # 由于个个人的文档不规范，这里强制使用另外的蠢方法
        # lin_ans_lin = pt_l_a_l.findall(para.text)
        # print(para.text)
        # if len(lin_ans_lin) == 1:       # if one answers catch
        #     index += 1
        #     ans = pt_a.findall(lin_ans_lin[0])[0]
        #     tmp = ch2num(ans)
        #     answers.append(tmp)
        #     # print the index and corresponding answer
        #     # print('抽取到第{}答案：{}'.format(index, ans))

        # 蠢方法1：（判断有横线，然后提取ABCD）
        # text = para.text
        # if '_' in text:
        #     ans = pt_a.findall(text)
        #     if len(ans) == 0:
        #         answers.append(-1)                   # if not detected marked as -1
        #         is_mark = True
        #         continue
        #     ans = ans[0]
        #     tmp = ch2num(ans)
        #     answers.append(tmp)
        #     index += 1

        # 蠢方法2：找到模型： "第[0-9]题", 然后找到第一个出现的字母
        text = para.text
        # print(text)
        if text.strip().startswith('A'):                # if reach the A........ then stop to find the answer
            is_find_sub = False
        subject = pt_sub.findall(text)
        if len(subject) == 1:                           # find subject
            is_find_sub = True
            sub_num = pt_sub_num.findall(subject[0])
            if not is_find_ans and len(answers) != 0:   # if not find the corresponding answer set -1 instead
                answers.append(-1)

        if is_find_sub:
            ans = pt_a.findall(text)
            if len(ans) >= 1:
                # if index == sub_num:
                ans = ans[-1]
                # print('题目：{}，检测序号：{}， 答案：{}'.format(sub_num, index + 1, ans))
                tmp = ch2num(ans)
                answers.append(tmp)
                is_find_sub = False
                is_find_ans = True
                index += 1

    # step 3:
    if index >= total_sub - 10:                             # if the detected num is reach a level , not to review
        is_mark = False
    if is_mark:
        print('mark, 文件名：{}'.format(f.name))

    # step 4: judge the index num and given total subject num
    if index >= total_sub - 10:
        print("抽取完毕，个数为：{}".format(index))
        return [answers, False]
    else:
        print("题目数量差太多，检查文档！")
        print('检测到的题目个数为：{}'.format(len(answers)))
        return [answers, True]


if __name__ == '__main__':
    file = open('C:\\Users\\lenovo02\\Documents\\WeChat Files\\Zipcoder\\Files\\第五章\\学生提交\\F110_192.168.117.110\\18120318叶宜宁.docx', 'rb')
    extract(file, 30)
