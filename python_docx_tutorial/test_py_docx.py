from docx import Document
import re


if __name__ == '__main__':
    text = "在Excel中，下面对于自定义自动筛选说法中不正确的是"     # ___C_____。
    lin_ans_lin = r"_[A-D]_"
    pt = re.compile(lin_ans_lin)
    lin_ans_lin = pt.findall(text)
    print(lin_ans_lin)

    f = open('第五章数据管理与分析-17113123-肖政恺.docx', 'rb')
    doc = Document(f)
    print(doc)
    index = 1
    for para in doc.paragraphs:
        print(str(index) + '段\t' + para.text)
        index += 1
