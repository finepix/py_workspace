import requests
import json

request_ip = 'http://2.2.2.2/ac_portal/default/pc.html?tabs=pwd'
login_url = 'http://2.2.2.2/ac_portal/login.php'

headers = {
    'Host': '2.2.2.2',
    'Connection': 'keep-alive',
    'User-Agent': '*/*',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type':  'application/json; charset=UTF-8',
    'Referer': 'http://2.2.2.2/ac_portal/20180625125820/pc.html'
}

# post_data = 'opr=pwdLogin&userName=14108438&pwd=Hdu1247430&rememberPwd=0'
post_data = {
    'opr': 'pwdLogin',
    'UserName': '14108438',
    'pwd': 'Hdu1247430',
    'rememberPwd': '0'
}

cookies = {
    'AUTHSESSID': '7568d2480e09',
    'AUTHSESSID': '51725622b754'
}


def get_ac_url():
    # 打开session
    session = requests.session()
    response = session.get(request_ip, headers=headers)
    # print(response.text)
    # 获取sessionID
    print('cookies:{}'.format(response.cookies.get_dict()))
    # cookies = response.cookies.get_dict()
    response = session.post(login_url, headers=headers, cookies=cookies, data=json.dumps(post_data))
    print(response.text)
    print('cookies:{}'.format(response.cookies.get_dict()))


if __name__ == '__main__':
    get_ac_url()
