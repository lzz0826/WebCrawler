import urllib.request
import urllib.parse

base_url = "https://www.baidu.com/s?wd=ip"

# 遇到汉字 可以使用parse.quote (GET请求) 转成 unicode编码格式
ch = urllib.parse.quote("汉字")
data = {
    'name' : '汉字',
    'sex' : '男'
}
chs = urllib.parse.urlencode(data)
# base_url = base_url + '?' = ch OR chs


# 添加请求头 订制请求对象是反爬的第一手段
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
httpRequest = urllib.request.Request(url=base_url, headers=headers)

# 代理ip
proxy = {
    'https':'185.32.6.131:8070'
}


response = None
try:
    # 模拟浏览器打开网页 response(HTTPResponse)response
    response = urllib.request.urlopen(httpRequest)

    # 使用代理
    # handler = a_urllib.request.ProxyHandler(proxy)
    # opener = a_urllib.request.build_opener(handler)
    # response = opener.open(httpRequest)

except urllib.error.HTTPError as e:
    print(f'HTTPError: {e.code}, Reason: {e.reason}')
    print(f'Response body: {e.read().decode("utf-8")}')  # 如果需要查看响应内容


# -----      response   -----------
# read() 返回二进制
readContent = response.read().decode('utf-8')
readlineContent = response.readline()
readlineContents = response.readlines()
httpCodeContent = response.getcode()
urlContent = response.geturl()
hearersContent = response.getheaders()
print(hearersContent)


# -----      下载   -----------

urllib.request.urlretrieve(base_url,'./download/'+'myFilename.html')

url_img = 'https://memeprod.ap-south-1.linodeobjects.com/user-template-thumbnail/a17e96b7884bba60c0a2cf9b27f8ee48.jpg'

# a_urllib.request.urlretrieve(url_img,'myImg.jpg')

url_video =''

# a_urllib.request.urlretrieve(url_video,'myVideo.mp4')




