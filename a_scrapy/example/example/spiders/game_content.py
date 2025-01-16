import time
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.http import HtmlResponse
from ..items import ExampleItem
import json



class BaiduSpider(scrapy.Spider):

    # 爬虫名 用于运行时使用
    name = "game_content"

    # 允许访问的域名
    allowed_domains = ["forum.gamer.com.tw","fanyi.baidu.com"]

    # 首页
    front_page = 'https://forum.gamer.com.tw'

    # 起始url地址
    start_urls = ["https://forum.gamer.com.tw/B.php?page=1&bsn=18966"]

    # 前缀
    basic_url = 'https://forum.gamer.com.tw/B.php?page='

    # 后缀
    suffix_url = '&bsn=18966'

    # 起始页
    start_page = 1
    # 结束页
    end_page = 5

    # 使用 Selenium 请求 解决懒加载问题
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    # GET 请求
    def parse(self, response):
        pass

        # ------ 确保懒加载完成
        # 获取 Selenium 驱动
        driver = response.meta['driver']

        # 滚动页面的 JavaScript
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待加载
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # 如果高度未变化，停止滚动
                break
            last_height = new_height

        # 获取下拉后的完整 HTML
        page_source = driver.page_source

        # 使用 Scrapy 的 HtmlResponse 重新封装 Selenium 获取的 HTML
        response = HtmlResponse(
            url=driver.current_url,
            body=page_source,
            encoding='utf-8'
        )
        # ------ 确保懒加载完成

        bas = response.xpath('//table[@class="b-list"]//tr[@class="b-list__row b-list-item b-imglist-item"]')

        print('-----------------------------')

        for b in bas:
            # 使用相对路径提取当前列表项的内容
            title = b.xpath('.//p[@class="b-list__main__title"]/text()').extract_first()
            img = b.xpath('.//div[@class="b-list__img lazyloaded"]/@data-thumbnail').extract_first()
            content = b.xpath('.//p[@class="b-list__brief"]/text()').extract_first()
            # 输出提取的内容
            print(f"标题: {title}")
            print(f"图片链接: {img}")
            print(f"内容摘要: {content}")

            # 第二层 页面
            second_url = b.xpath('.//p[@class="b-list__main__title"]/@href').get()

            second_url = self.front_page + '/' + second_url

            # meta 可将 上层参数传递给下层页面解析器
            yield SeleniumRequest(url=second_url, callback=self.second,meta={
                'title' : title,
                'img' : img,
                'content' : content,
            })

        # 循环多页
        if self.start_page < self.end_page:
            self.start_page = self.start_page + 1

            url = self.basic_url + str(self.start_page) + self.suffix_url

            url = f"{self.basic_url}{self.start_page}{self.suffix_url}"

            # 使用 SeleniumRequest 处理分页请求
            yield SeleniumRequest(url=url, callback=self.parse)

            # #scrapy.Request scrapy的get请求
            # #调用 parse方法 callback 是要执行哪个函数
            # # meta 可将 上层参数传递给下层页面解析器
            # yield scrapy.Request(url=url,callback=self.parse,meta={})

    # 内容页
    def second(self, response):
        title = response.meta['title']
        img = response.meta['img']
        content = response.meta['content']
        userName = response.xpath('//div[@class="c-post__header__author"]/a[@class="username"]/text()').extract_first()

        # 创建 Item 物件
        item = ExampleItem(title = title,img = img,content = content,userName = userName)
        # 每获取一个 交给 pipelines 管道
        yield item

    # POST 请求 *POST 不关 start_urls 和 parse
    # 可以使用 scrapy 提供 start_requests 在启动时发起 也可以自订函数 给其他地方调用使用 scrapy.FormRequest
    # def start_requests(self):
    #
    #     url = 'https://fanyi.baidu.com/sug'
    #     headers = {
    #         'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    #     }
    #     data = {
    #         'kw' : 'apple',
    #     }
    #     yield scrapy.FormRequest(url=url, headers=headers, formdata=data, callback=self.post_def)
    #
    # def post_def(self,response):
    #     content = response.text
    #     obj = json.loads(content)
    #     # obj = json.loads(content,encoding='utf-8')
    #     print(obj)

















