import scrapy


class BaiduSpider(scrapy.Spider):

    # 爬虫名 用于运行时使用
    name = "game"

    # 允许访问的域名
    allowed_domains = ["https://www.gamer.com.tw/"]

    # 起始url地址
    start_urls = ["https://www.gamer.com.tw/"]

    # 执行了start_urls之后 执行的方法 方法中的response就是返回的那个对象
    # 相当于 response = urllib.request.urlopen）
    #       response = requests.get()
    def parse(self, response):

        # 获取的是响应的字符串
        # content = response.text

        # 获取的是二进制数据
        # content = response.body

        # 可以直接是xpath方法来解析response中的内容
        content = response.xpath('//div[@id="BH-background"]//div[@id="gnnContainer"]//a[@class="bh-card card_headnews"]/div[@class="gnn-text"]/text()')[1]
        print("--------------------------------------------------------")

        # 提取seletor对象的data属性值
        print(content.extract())

        # 提取的seletor列表的第一个数据
        # print(content.extract_first)
        print("--------------------------------------------------------")
