import requests

# Base URL for Baidu search
base_url = "https://www.baidu.com/s?"

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

data = {
    'wd': '你好',  # 搜索关键字
}

# 使用代理
proxies = {
    'http': '185.32.6.131:8070',
}

response = requests.get(url=base_url, headers=headers, params=data, proxies=proxies)

response.encoding = 'utf-8'

print(response.text)
