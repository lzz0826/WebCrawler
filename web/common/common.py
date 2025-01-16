from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from web.db.mypql.db_mysql import count_data
from web.config.yaml_config import Global
from datetime import datetime
from web.common.java_api import isPostExisted



# 檢查重複
def check_repeat(source, article_id):
    count = count_data(source, article_id)
    is_postExisted = isPostExisted(source, article_id)
    if count >= 1 or is_postExisted:
        return True
    else:
        return False



def get_current_timestamp():
    new_time = datetime.now()
    return int(new_time.timestamp() * 1000)

def get_request_headers():
    browsermob_path = Global['browsermob_path']
    print(browsermob_path)
    # 开启Proxy
    server = Server(r'' + browsermob_path + '')
    server.start()
    proxy = server.create_proxy()

    # 配置Proxy启动WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # 解决 您的连接不是私密连接问题
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-urlfetcher-cert-requests')

    # 背景模式
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(20)

    proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})

    driver.get("https://www.youtube.com/")

    result = proxy.har

    entries = result['log']['entries']

    for entry in entries:
        request = entry['request']
        headers = request['headers']

        # 获取指定请求的头部信息
        if request['url'] == 'https://www.youtube.com/' and request['method'] == 'GET':
            print('Request Headers:')
            for header in headers:
                name = header['name']
                value = header['value']
                print(f'{name}: {value}')

            break
