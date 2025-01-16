# Scrapy settings for example project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "example"

SPIDER_MODULES = ["example.spiders"]
NEWSPIDER_MODULE = "example.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "example (+http://www.yourdomain.com)"

# Obey robots.txt rules 君子协议 建议关闭
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "example.middlewares.ExampleSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "example.middlewares.ExampleDownloaderMiddleware": 543,
#}


# 日志级别
# LOG_LEVEL = "DEBUG"
# 保存日志路径
LOG_FILE = "../log/example.log"

# 启用 Scrapy Selenium 的中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

# MYSQL 配置
DB_HOST = '169.254.38.183'
# 端口号是一个整数
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
# 数据库名称
DB_NAME = 'spider01'
DB_CHARSET = 'utf8'


# 使用 Chrome 浏览器
SELENIUM_DRIVER_NAME = 'chrome'
# 自动获取 ChromeDriver
SELENIUM_DRIVER_EXECUTABLE_PATH = '/Users/sai/.wdm/drivers/chromedriver/mac64/131.0.6778.264/chromedriver-mac-arm64/chromedriver'  # 在 Spider 中通过 `ChromeDriverManager` 动态配置
# 可选的 Chrome 启动参数（无头模式）
SELENIUM_DRIVER_ARGUMENTS = ['--headless']


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #  管道优先及 1 - 1000 越小越高
   "example.pipelines.ExamplePipeline": 300,
   "example.pipelines.ExampleDownloadImg": 301,
   #  MYSQL 管道
   # 'example.pipelines.MysqlPipeline': 302,
}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
