import requests


url = 'https://www.youtube.com/watch?v=tN-60dIgt60&list=PLmOn9nNkQxJH39Kc0suTsx7qxMGc_Cp1-&index=85'


requests = requests.get(url = url)
# 一个类型 六个属性
# Response 类型
# print(type(requests))

# 设置想印编码格式
requests.encoding = 'utf-8'

# 返回网页原码 String
# print(requests.text)

# 返回url
# print(requests.url)

# 返回二进制数据
# print(requests.content)

# 返回HTTP状态马
# print(requests.status_code)

# 返回响应头
print(requests.headers)




