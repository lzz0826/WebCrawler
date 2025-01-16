import requests
from bs4 import BeautifulSoup
import os
import time
import datetime
import random
import logging
from web.common.java_api import post_admin_ghostPost_addWithTorrent
from web.vo.add_with_torrent import Add_With_Torrent
from web.common.anti_anti_apider import Anti_Anti_Spider
from web.db.mypql.db_mysql import insert_data
from web.do.article_DO import Article_DO
from web.config.yaml_config import Global
from web.config.logging_config import configure_logging
configure_logging()


# 設定代理ip要撈多少
ip_number = 2

# 來源名
sourece_name = 't66y'

# url前綴
url_prefix = 'https://www.t66y.com/'

# 下載前綴
download_prefix = 'www.rmdown.com/link.php'

# Python 的内置 HTML 解析器
features = 'html.parser'

headers_google = {
    'authority': 'www.rmdown.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'cookie': 'PHPSESSID=kvhbnqrhpduh4ee1n2l2ajnsv1; ses=06ed9eb665856d8f5642bef92acfde6a',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

headers_ie = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-CN;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=pls3b0vtmrjjgn74opub98mtk3; ses=e165bec36d8f9102aadad4a258aceb52",
    "Host": "www.rmdown.com",
    "Referer": "http://www.rmdown.com/link.php?hash=232eac268b20b8203636a4060970bb8968f24923eec",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51"
}

anti_anti_spider = Anti_Anti_Spider(ip_number, headers_google, headers_ie)


class MainPage:
    def __init__(self, district_name, district_url):
        self.district_name = district_name
        self.district_url = district_url


class District:
    def __init__(self, article_id, title, content_url):
        self.article_id = article_id
        self.title = title
        self.content_url = content_url


class Content:
    def __init__(self, text, images, download_url):
        self.text = text
        self.images = images
        self.download_url = download_url





# 主頁面頁面
def main_page(url, headers):
    if not (url):
        return None
    try:
        main_page_list = []
        res = requests.get(url, headers=headers, proxies=anti_anti_spider.proxy)
        print(res)
        soup = BeautifulSoup(res.text, features=features)
        for item in soup.select('#cate_1 .tr3'):
            h2 = item.find('h2')
            a = h2.find('a')
            name = a.text
            url = url_prefix + a.get('href')
            main_page = MainPage(name, url)
            if url != 'https://www.t66y.com/thread0806.php?fid=27' and url != 'https://www.t66y.com/thread0806.php?fid=10':
                main_page_list.append(main_page)
    except Exception as e:
        logging.info("ˊ主頁面出现错误:", e)
        return None
    return main_page_list


# 主頁面递归
def fetch_main_pages(headers):
    if anti_anti_spider.proxy.get('http') is None or anti_anti_spider.proxy.get('http') == '':
        anti_anti_spider.set_random_proxy()
    main_pages = main_page('https://www.t66y.com/index.php', headers)
    if main_pages is None or main_pages == []:
        anti_anti_spider.remove_random_ip()
        return fetch_main_pages(headers)
    return main_pages


# 區域頁面
def districts_page(url, headers):
    if not (url):
        return None

    try:
        res = requests.get(url, headers=headers, proxies=anti_anti_spider.proxy)
        soup = BeautifulSoup(res.text, features=features)
        district_list = []
        for item in soup.select('#tbody .tal h3'):
            a = item.find('a')
            article_id = a.get('id')
            title = a.text.strip()
            href = a.get('href')
            district = District(article_id, title, url_prefix + href)
            district_list.append(district)
    except Exception as e:
        logging.info("區域頁面出现错误:", e)
        return None
    return district_list


# 區域頁面递归
def fetch_districts_page(url, headers):
    districts_pages = districts_page(url, headers)
    if districts_pages is None or districts_pages == []:
        anti_anti_spider.remove_random_ip()
        return fetch_districts_page(url, headers)
    return districts_pages


# 內容頁面
def content_page(url, headers):
    if not (url):
        return None
    try:
        res = requests.get(url, headers=headers, proxies=anti_anti_spider.proxy)
        soup = BeautifulSoup(res.text, features=features)
        for item in soup.select('#conttpc'):
            download_url = ''
            text = str(item.findAll)
            soup = BeautifulSoup(text, 'html.parser')
            img_tags = soup.find_all('img')
            image_urls = []
            for img in img_tags:
                if 'ess-data' in img:
                    img['src'] = img['ess-data']
                    del img['ess-data']
                image_urls.append(img.get('src'))
            modified_text = str(soup)
            for a_tag in item.find_all('a'):
                href = a_tag.get('href')
                if href and download_prefix in href:
                    download_url = href
                    break

            content = Content(modified_text, image_urls, download_url)
            if content is None:
                return None
            else:
                return content
    except Exception as e:
        logging.info("內容頁面时出现错误:", e)
        return None


# 下載頁面
def download_page(url, headers):
    if not (url):
        return None

    try:
        res = requests.get(url, headers=headers, proxies=anti_anti_spider.proxy)
        soup = BeautifulSoup(res.text, features=features)
        hidden_inputs = soup.find_all("input", type="hidden")  # 查找所有隐藏输入字段
        reff = ''
        ref = ''
        for hidden_input in hidden_inputs:
            name = hidden_input.get("name")  # 获取字段名
            value = hidden_input.get("value")  # 获取字段值
            if name == 'ref':
                ref = value
            if name == "reff":
                reff = value
        urlee = 'https://www.rmdown.com/download.php?des=cd-sgfeks&esc=raso-3msi&axs=4js-oowqa&reff=' + reff + '&ref=' + ref
        print("urlee:", urlee)
    except Exception as e:
        logging.info("下載頁面时出现错误:", e)
        return None
    return urlee


# 下載
def download_file(url, save_directory, file_name, headers):
    if not (url and save_directory and file_name):
        return None

    try:
        folder_path = os.path.join(save_directory, file_name)  # 创建新文件夹的路径
        os.makedirs(folder_path, exist_ok=True)  # 创建文件夹，如果已存在则不创建
        file_name = file_name + '.torrent'
        save_path = os.path.join(folder_path, file_name)  # 新的保存路径
        response = requests.get(url, headers=headers, stream=True, proxies=anti_anti_spider.proxy)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    except Exception as e:
        logging.info("下载文件时出现错误:", e)
        return None
    return folder_path



# --------------------主要執行----------

def t66y_main():
    logging.info("T66Y啟動")
    anti_anti_spider.get_iplist()
    headers = anti_anti_spider.random_headers()

    # 主頁面
    main_pages = fetch_main_pages(headers)

    for main_page in main_pages:


        district_url = main_page.district_url
        tags = main_page.district_name
        counter = 0
        while counter <= int(Global.yml_data['t66y']['cycles']):


            sleep_time = random.randint(int(Global.yml_data['t66y']['sleep_time_min']), int(Global.yml_data['t66y']['sleep_time_mix']))

            page = counter + 1
            # 區域頁面
            res_district_list = districts_page(district_url + "&search=&page=" + str(page), headers)

            if res_district_list is None or res_district_list == []:
                counter += 1
                continue

            for res_district in res_district_list:

                headers = anti_anti_spider.random_headers()
                article_id = res_district.article_id

                title = res_district.title
                content_url = res_district.content_url

                # 內容頁面
                content = content_page(content_url, headers)
                if content is None:
                    continue
                content_text = content.text
                images = content.images
                download_url = content.download_url

                # 下載頁面
                res_download_url = download_page(download_url, headers)
                if res_download_url is None or res_download_url == '':
                    continue

                current_directory = str(Global.yml_data['t66y']['current_directory'])

                # 下載
                download_file_path = download_file(res_download_url, current_directory, article_id, headers)
                if download_file_path is None or download_file_path == '':
                    continue

                # 存DB TODO 雪花 .狀態
                article_do = Article_DO(1, sourece_name, article_id, title, tags, content_text, images, content_url, download_url,
                            download_file_path, 0, '測試',
                            datetime.datetime.now()
                            , datetime.datetime.now())
                insert_data(article_do)

                # 打API
                add_with_torrent = Add_With_Torrent(sourece_name, article_id, title, content_text, tags, content_url, download_file_path,
                                article_id)
                post_admin_ghostPost_addWithTorrent(add_with_torrent)

                time.sleep(sleep_time)

            counter += 1

if __name__ == '__main__':
    t66y_main()