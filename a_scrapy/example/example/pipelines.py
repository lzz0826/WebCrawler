# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from urllib import request
# 加载settings文件
from scrapy.utils.project import get_project_settings
import pymysql


# pipelines 下载数据 * 需要打开 ITEM_PIPELINES 多调管道需要到 settings.py 添加
# items 定义数据结构
class ExamplePipeline:
    # 爬虫开时之前
    def open_spider(self,spider):
        print("-----------爬虫开时之前----------------")
        self.fp = open('../download/json/geme.json', 'w', encoding='UTF-8')

    # 下载文件 item 就是 yield item 传来的对象
    def process_item(self, item, spider):

        # # w 模式会覆盖 用 a 模添加  *这里会导致平凡开关不推荐
        # with open('geme.json', 'a', encoding='UTF-8') as fp:
        #     # write 只能String 不能是其他对象
        #     fp.write(str(item))
        self.fp.write(str(item))
        return item

    # 爬虫开时之后
    def close_spider(self,spider):
        print("-----------爬虫开时之后----------------")
        self.fp.close()

# 管道2下载图片
class ExampleDownloadImg:
    # 下载图片
    def process_item(self, item, spider):
        url = item.get('img')
        if url != None:
            filename = '../download/imgs/' + item.get('title') + '.jpg'
            request.urlretrieve(url=url, filename=filename)
        return item


# MYSQL 管道
class MysqlPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        self.coonect()

    # 自定义函数
    def coonect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.name, charset=self.charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into book(name,src) values("{}","{}")'.format(item['name'], item['src'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 提交
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
