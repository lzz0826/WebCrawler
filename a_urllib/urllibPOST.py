import urllib.request
import urllib.parse
import urllib.error
import json

# base_url = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute?rpcids=rPsWke&source-path=%2F&f.sid=1373070675576063320&bl=boq_translate-webserver_20250105.08_p0&hl=zh-cn&soc-app=1&soc-platform=1&soc-device=1&_reqid=1849580&rt=c"
base_url = "https://translate.google.com/_/TranslateWebserverUi/data"
# base_url = "https://sdfgdfsgdfgre4.google.com/_/TranslateWebserverUi/data"


# 添加请求头 订制请求对象是反爬的第一手段
# 注意参数会影响接收编码 'Accept-Encoding' : 'gzip , deflate, br'
# 有些会要求必要请求头 如:Cookie
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    # 'cookie' : '', 夹带验证讯息
    # 'referer' : '' 判断当前路径是否由上个路径进来的 一般做图片防盗练
}

# POSY 请求参数 必需编码 .urlencode(data).encode('utf-8')
data = {
    'f.req':'[[["rPsWke","[[apple,en,zh-TW],1]",null,"generic"]]]'
}
data = urllib.parse.urlencode(data).encode('utf-8')



content = None
try:
    httpRequest = urllib.request.Request(url=base_url, data=data, headers=headers)

    # 模拟浏览器打开网页 response(HTTPResponse)
    response = urllib.request.urlopen(httpRequest)

    content = response.read().decode('utf-8')

# HTTPError
except urllib.error.HTTPError as e:
    print(f'HTTPError: {e.code}, Reason: {e.reason}')
    print(f'Response body: {e.read().decode("utf-8")}')  # 如果需要查看响应内容

# URLError
except urllib.error.URLError as e:
    print(f'URLError: Reason: {e.reason}')



# 转json对象
# obj = json.loads(content)
print(content)
print(type(content))
# print(obj)



