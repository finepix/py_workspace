from selenium import webdriver
import time
import os


url = 'http://2.2.2.2'
user_name = '181050016'
pwd = '0016247430'


def login():
    """
            校园上网验证
    :return:
    """
    # initialization
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    # chrome_driver/chromedriver.exe
    browser.get(url)
    login_btns = browser.find_element_by_id('mode_password')\
        .find_element_by_css_selector('.login_body > .btn_ok')\
        .find_elements_by_class_name('login_btn')

    # login in
    btn = login_btns.pop(0)
    btn.click()

    # fill pwd and user name
    input_btn_user_name = browser.find_element_by_id('password_name')
    input_btn_user_name.clear()
    for ch in user_name:
        input_btn_user_name.send_keys(ch)
        time.sleep(0.3)

    input_btn_pwd = browser.find_element_by_id('password_pwd')
    input_btn_pwd.clear()
    for ch in pwd:
        input_btn_pwd.send_keys(ch)
        time.sleep(0.3)

    # 提交
    submit_btn = browser.find_element_by_id('password_submitBtn')
    submit_btn.click()

    # 关闭浏览器
    time.sleep(1)
    browser.close()


def is_online():
    """
                判断当前是否可连接网络
    :return:
    """
    test_domain = 'www.baidu.com'
    cmd = 'ping ' + test_domain
    exit_code = os.system(cmd)
    if exit_code:
        return False
    else:
        return True


if __name__ == '__main__':

    # 服务未开启
    login()
    while True:
        if is_online():
            print('设备已联网，等待20分钟重新检测')
            time.sleep(1200)
        else:
            print('设备不在线，启动注册程序！')
            login()
            print('注册成功，已联网。')
