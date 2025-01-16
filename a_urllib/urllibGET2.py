import urllib.request
import urllib.parse

def dd(page):
    print("{a},{b} and {c} are my friends.".format(a='Sean', b='John', c='Luis'))
    # John,Luis and Sean are my friends.

    data = {
        'page':(page-1)*20,
        'limit' : 20
    }

    req = urllib.parse.urlencode(data)


    base_url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&"

    url = base_url + req

    print(url)

    # 添加请求头 订制请求对象是反爬的第一手段
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    httpRequest = urllib.request.Request(url=url, headers=headers)

    # 模拟浏览器打开网页 response(HTTPResponse)
    response = urllib.request.urlopen(httpRequest)

    content = response.read().decode('utf-8')

    # 下载数据JSON
    # f = open('myJson.json','w',encoding='utf-8')
    # f.write(content)
    with open('myJson.json', 'w', encoding='utf-8') as fp:
        fp.write(content)


if __name__ == '__main__':
    dd(4)








