from selenium import webdriver
import time

# initialization
browser = webdriver.Chrome('chrome_driver/chromedriver.exe')
url = 'http://2.2.2.2'
user_name = '181050016'
pwd = '0016247430'


def login():
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


if __name__ == '__main__':
    login()
