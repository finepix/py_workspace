import requests

post_url = 'http://2.2.2.2/ac_portal/login.php'
url = 'http://2.2.2.2/'
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


def main():
    r = requests.post(post_url, headers=headers, json=post_data)
    print(r.text)


if __name__ == '__main__':
    main()
