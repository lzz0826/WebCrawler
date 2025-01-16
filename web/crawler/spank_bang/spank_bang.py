import argparse
import asyncio
import time

from bs4 import BeautifulSoup
from web.common.java_api import post_admin_ghostPost_addWithDwLink
from web.util.download_util import download_mp4
from web.common.common import check_repeat
from web.db.mypql.db_mysql import insert_data, insert_analyze
from web.common.uploader import upload_file_mega
from web.config.yaml_config import Global
from web.vo.add_with_dw_link_VO import Add_with_dw_link_VO
from web.do.article_DO import Article_DO
from web.do.article_analyze_DO import Article_Analyze_DO
from web.util.snow_flake import get_snow_id
import logging
import cloudscraper
import datetime
from web.config.logging_config import configure_logging

configure_logging()

# 來源
source = 'spank bang'

# Python 的内置 HTML 解析器
features = 'html.parser'

# url前綴
url_prefix = 'https://spankbang.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}


class Main_page:

    def __init__(self, id, content_url):
        self.id = id
        self.content_url = content_url


class ContentPage:
    def __init__(self, video_id, title, mp4_url, tags, img):
        self.video_id = video_id
        self.title = title
        self.mp4_url = mp4_url
        self.tags = tags
        self.img = img


# 主頁面
def main_page(url):
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get(url)
        soup = BeautifulSoup(res.text, features=features)
        logging.info(res)

        main_page_list = []

        for item in soup.select('#browse_new .video-list'):
            for div in item.findAll('div'):
                id = div.get('id')
                if id is not None or id != '':
                    a_tags = div.find_all('a')
                    href_set = set()
                    for a in a_tags:
                        href = a.get('href')
                        if href not in href_set:
                            url = str(url_prefix + href)
                            main_page = Main_page(id, url)
                            main_page_list.append(main_page)
                            href_set.add(href)
        return main_page_list
    except Exception as e:
        logging.info("主頁出现错误:", e)
        return None


# 主頁面遞歸
def fetch_main_pages(url):
    main_page_list = main_page(url)
    while main_page_list is None or main_page_list == []:
        main_page_list = main_page(url)
        time.sleep(1)
    return main_page_list


# 內容頁面
def content_page(url):
    if url is None or url == '':
        return None
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get(url)
        soup = BeautifulSoup(res.text, features=features)
        print(res)
        tags = []
        for item in soup.select('#container'):
            video_id = item.select_one('#video').get('data-videoid')
            img = item.find('img').get('src')
            title = item.find('h1').text
            searches = item.select('.searches a')
            if searches is not None or searches != []:
                for a in searches:
                    tags.append(a.text)
            video_container = item.select_one('#video_container')
            source = video_container.find('source')
            src = source.get('src')
        content = ContentPage(video_id, title, src, tags, img)
        return content
    except Exception as e:
        logging.info("內容出现错误:", e)
        return None


# 內容頁面遞歸
def fetch_content_page(url, try_content_pag):
    content = content_page(url)
    attempts = 0
    while content is None and attempts < try_content_pag:
        time.sleep(1)
        content = content_page(url)
        attempts += 1
    return content


def spank_bang_main():
    logging.info("SpankBang啟動")
    # 主頁面
    url = 'https://spankbang.com/new_videos/'
    main_page_list = fetch_main_pages(url)

    for main_page in main_page_list:
        id = main_page.id
        content_url = main_page.content_url

        # 內容頁
        content = fetch_content_page(content_url, int(Global.yml_data['spank_bang']['try_content_pag']))
        if content is None or content == '':
            continue
        video_id = content.video_id
        title = content.title
        mp4_url = content.mp4_url
        tags = content.tags
        img = content.img

        current_directory = str(Global.yml_data['spank_bang']['current_directory'])

        # 檢查是否下載過
        if check_repeat(source, video_id):
            logging.info('以下載過')
            continue

        # 下載
        download_rep = download_mp4(mp4_url, title, current_directory, headers,
                                    int(Global.yml_data['spank_bang']['set_file_size_mb']))
        if download_rep is None:
            continue
        file_name = download_rep.file_name
        folder_path = download_rep.folder_path
        download_start_time = download_rep.download_start_time
        download_end_time = download_rep.download_end_time
        file_size = download_rep.size
        md5 = download_rep.md5

        # 上傳免空
        file_path = str(folder_path + '/' + title + '.mp4')
        upload_rep = asyncio.run(upload_file_mega(file_path, str(Global.yml_data['spank_bang']['upload_file_path'])))
        if upload_rep is None:
            continue

        provider = upload_rep.provider
        upload_start_time = upload_rep.upload_start_time
        upload_end_time = upload_rep.upload_end_time



        # 進資料庫
        article_do = Article_DO(get_snow_id(), source, video_id, title, tags, title, img, url_prefix, mp4_url, folder_path
                                , '1', '備註', datetime.datetime.now(), datetime.datetime.now())
        insert_data(article_do)

        article_analyze_do = Article_Analyze_DO(get_snow_id(), video_id, source, provider, file_size, md5,
                                                upload_start_time, upload_end_time, download_start_time, download_end_time)
        insert_analyze(article_analyze_do)


        # 打java API
        vo = Add_with_dw_link_VO(source, video_id, title, file_name,title ,tags, url_prefix, mp4_url, provider, file_size, upload_start_time,
                                 upload_end_time, download_start_time, download_end_time,md5)
        post_admin_ghostPost_addWithDwLink(vo)

        time.sleep(int(Global.yml_data['spank_bang']['cycle_time']))


if __name__ == "__main__":
    logging.info("Spank Bang測試啟動")
    parser = argparse.ArgumentParser()
    parser.add_argument('--yml', help='設置yml位置')
    args = parser.parse_args()

    # 加載環境變量
    Global.load_yaml_file(args.yml)

    spank_bang_main()
