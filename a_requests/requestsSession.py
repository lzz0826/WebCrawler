"""
cookie登陆古诗文网（含验证码）
"""
# 通过登陆  然后进入到主页面

# 通过找登陆接口我们发现 登陆的时候需要的参数很多
# __VIEWSTATE: wzavkIiUpeGeXT-Gu4jEWSBcHAneSt4SJdDa3y/PEP5sDZuLEWgE1r37kEQzlJ/pVVbYYMe7vrMvtm3NUmkX2KGAuPYULzyiZDcfhry5nbmFCtGY/RrDbqJIDMu0KDOYRMeQRs/Xwv2vH/1ZpkEoSK0lGoA0=
# __VIEWSTATEGENERATOR: C93BE1AE
# from: http://so.gushiwen.cn/user/collect.aspx
# email: cney6tcn@linshiyouxiang.net
# pwd: 8YW8GYET78933ETR
# code: 32GV
# denglu: 登录

# 我们观察到__VIEWSTATE   __VIEWSTATEGENERATOR  code是一个可以变化的量

# 难点:(1)__VIEWSTATE   __VIEWSTATEGENERATOR  一般情况看不到的数据 都是在页面的源码中
#     我们观察到这两个数据在页面的源码中 所以我们需要获取页面的源码 然后进行解析就可以获取了
#     (2)验证码

import requests
from bs4 import BeautifulSoup
import urllib.request

# 这是登陆页面的url地址
url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.a'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) Ap-pleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.200',
}
response = requests.get(url=url, headers=headers)
content = response.text
# print(content)  # 测试代码，验证能否获取网页源码

# 解析页面源码  然后获取__VIEWSTATE   __VIEWSTATEGENERATOR
soup = BeautifulSoup(content, 'lxml')

# 获取__VIEWSTATE
# .select返回列表，需用切片取出对应标签      .attrs.get获取属性值
viewstate = soup.select('#__VIEWSTATE')[0].attrs.get('value')

# 获取__VIEWSTATEGENERATOR
viewstategenerator = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

# print(viewstate)  # 测试代码，验证是否获取到__VIEWSTATE的参数
# print(viewstategenerator)  # 测试代码，验证是否获取到__VIEWSTATEGENERATOR的参数

# 获取验证码图片
code_url_para = soup.select('#imgCode')[0].attrs.get('src')
code_url = 'https://so.gushiwen.cn/' + code_url_para
# print(code_url)  # 测试代码，验证是否获取到验证码的图片的url

# 有坑
# (1)在浏览器的检查的网络里找登陆接口时，如果不勾选检查的网络里的保留日志
# 且输入正确的名字、正确的密码、正确的验证码并登陆后，老版浏览器或者可能别的浏览器会
# 出现登陆接口会消失的情况，  进而导致无法寻找到登陆接口
# (2)“urllib.request.urlretrieve”下载图片提交的请求和“requests.post”提交的请求不是同一个，
# 会导致“requests.post”提交的请求时，程序端输入的验证码失效
# requests里面有一个方法 session()  通过session的返回值 就能使用请求变成一个对象
# urllib.request.urlretrieve(url=code_url, filename='code.jpg')
session = requests.session()
# 验证码的url的内容
response_code = session.get(code_url)
# 注意此时要使用二进制数据，通过二进制下载图片
content_code = response_code.content
# wb的模式就是将二进制数据写入到文件
with open('code.jpg', 'wb') as fp:
    fp.write(content_code)

# 获取了验证码的图片之后 下载到本地 然后观察验证码 观察之后 然后在控制台输入这个验证码
# 就可以捋这个值给code的参数 就可以登陆
code_name = input('请输入你的验证码')

# 点击登陆
url_post = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
data_post = {
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'from': 'http://so.gushiwen.cn/user/collect.aspx',
    'email': 'cney6tcn@linshiyouxiang.net',
    'pwd': 'u89w7829e',  # 此处请输入正确的密码
    'code': code_name,
    'denglu': '登录',
}

response_post = session.post(url=url_post, headers=headers, data=data_post)
content_post = response_post.text

with open('古诗文.html', 'w', encoding='UTF-8') as fp:
    fp.write(content_post)

# 难点
# （1） 隐藏域
# （2） 验证码

