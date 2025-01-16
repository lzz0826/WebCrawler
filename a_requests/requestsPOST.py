import requests


base_url = "https://fanyi.baidu.com/sug"

headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

data = {
    'kw' : 'apple',
}

response = requests.post(url=base_url,data=data,headers=headers)
obj = response.json()
print(obj)
print(type(obj))

