import argparse
import asyncio
import uuid

import requests
from bs4 import BeautifulSoup
import logging


from web.config.yaml_config import Global

from web.common.common import check_repeat
from web.db.mypql.db_mysql import insert_data
from web.common.java_api import post_admin_ghostPost_addWithDwLink
from web.common.uploader import upload_file_mega
from web.do.article_DO import Article_DO
from web.util.download_util import download_yt
from web.vo.add_with_dw_link_VO import Add_with_dw_link_VO
from datetime import datetime

features = 'html.parser'
url_prefix = 'https://www.youporn.com'
source = 'youporn'
upload_file_path = '/youporn'


class Youporn:
    def __init__(self, video_id, title, video_page_url, tags):
        self.video_id = video_id
        self.video_page_url = video_page_url
        self.title = title
        self.tags = tags
        self.video_upload_url = None
        self.video_local_folder = None
        self.file_name = None
        self.file_size = 0
        self.upload_start_time = 0
        self.upload_end_time = 0
        self.download_start_time = 0
        self.download_end_time = 0
        self.md5 = ''

    def set_video_upload_url(self, video_upload_url):
        self.video_upload_url = video_upload_url

    def set_video_local_folder(self, video_local_path):
        self.video_local_folder = video_local_path

    def set_file_name(self, file_name):
        self.file_name = file_name

    def set_file_size(self, file_size):
        self.file_size = file_size

    def set_upload_start_time(self, upload_start_time):
        self.upload_start_time = upload_start_time

    def set_upload_end_time(self, upload_end_time):
        self.upload_end_time = upload_end_time

    def set_download_start_time(self, download_start_time):
        self.download_start_time = download_start_time

    def set_download_end_time(self, download_end_time):
        self.download_end_time = download_end_time

    def set_md5(self, md5):
        self.md5 = md5

    def get_view_key(self):
        return self.video_id

    def get_title(self):
        return self.title

    def get_video_page_url(self):
        return self.video_page_url

    def get_video_upload_url(self):
        return self.video_upload_url

    def get_video_local_folder(self):
        return self.video_local_folder

    def get_file_name(self):
        return self.file_name

    def get_file_size(self):
        return self.file_size

    def get_upload_start_time(self):
        return self.upload_start_time

    def get_upload_end_time(self):
        return self.upload_end_time

    def get_download_start_time(self):
        return self.download_start_time

    def get_download_end_time(self):
        return self.download_end_time

    def get_md5(self):
        return self.md5


def main_page(main_page_url, tags):
    if not main_page_url:
        return None
    youporn_list = []

    res = requests.get(main_page_url, proxies=None)
    soup = BeautifulSoup(res.text, features)

    for item in soup\
            .select('#mainContent '
                    '#advanced-filters '
                    '.searchResults.full-row-thumbs.row.js_video_row '
                    '.video-box.four-column.video_block_wrapper '
                    'a '):
        if '/watch/' not in item.get('href'):
            continue

        title_div = item.select_one('.video-box-title')
        if title_div is None:
            continue

        title = title_div.get('title')
        url = item.get('href')
        video_id = url.split('/')[2]

        video_page_url = url_prefix + url

        youporn = Youporn(video_id, title, video_page_url, tags)
        youporn_list.append(youporn)

    return youporn_list


def video_page(youporn):
    urls = [youporn.get_video_page_url()]
    proxy = ''
    video_name = youporn.get_view_key()
    mp4_dir = Global.yml_data['youporn']['mp4_dir']

    download_rep = download_yt(urls=urls, proxy=proxy, mp4_file_dir=mp4_dir, mp4_file_name=video_name)
    if download_rep is None:
        raise Exception('下載失敗')

    video_path = download_rep.folder_path
    file_name = download_rep.file_name
    file_size = download_rep.size
    download_start_time = download_rep.download_start_time
    download_end_time = download_rep.download_end_time
    md5 = download_rep.md5

    youporn.set_video_local_folder(video_path)
    youporn.set_file_name(file_name)
    youporn.set_file_size(file_size)
    youporn.set_download_start_time(download_start_time)
    youporn.set_download_end_time(download_end_time)
    youporn.set_md5(md5)

    return youporn


def upload_video(youporn):
    upload_rep = asyncio.run(upload_file_mega(youporn.get_video_local_folder(), upload_file_path))
    video_upload_url = upload_rep.link
    upload_start_time = upload_rep.upload_start_time
    upload_end_time = upload_rep.upload_end_time

    youporn.set_video_upload_url(video_upload_url)
    youporn.set_upload_start_time(upload_start_time)
    youporn.set_upload_end_time(upload_end_time)
    return youporn


def send_to_ghost(youporn):
    do = Article_DO(id=str(uuid.uuid4()),
                    source=source,
                    article_id=youporn.get_view_key(),
                    title=youporn.get_title(),
                    tags=None,
                    content='hello',
                    images=None,
                    source_url=youporn.get_video_page_url(),
                    download_url=youporn.get_video_upload_url(),
                    folder_path=youporn.get_video_local_folder(),
                    status=1,
                    memo=None,
                    update_time=datetime.now(),
                    create_time=datetime.now())
    insert_data(do)

    request = Add_with_dw_link_VO(source=source,
                                  article_id=youporn.get_view_key(),
                                  title=youporn.get_title(),
                                  file_name=youporn.get_file_name(),
                                  content='hello',
                                  tags=None,
                                  source_url=youporn.get_video_page_url(),
                                  dwLink=youporn.get_video_upload_url(),
                                  provider='mega',
                                  file_size=youporn.get_file_size(),
                                  upload_start_time=youporn.get_upload_start_time(),
                                  upload_end_time=youporn.get_upload_end_time(),
                                  download_start_time=youporn.get_download_start_time(),
                                  download_end_time=youporn.get_download_end_time(),
                                  md5=youporn.get_md5())
    post_admin_ghostPost_addWithDwLink(request)


def youporn_main():
    logging.info("Youporn 啟動")

    for page in range(1, 99):
        try:
            youporn_list = main_page('https://www.youporn.com/porntags/creampie/?page=' + str(page), ['CREAMPIE'])
            for youporn in youporn_list:
                if check_repeat(source, youporn.video_id):
                    print(source + '_' + youporn.video_id + '已經下載過')
                    continue
                try:
                    youporn = video_page(youporn)
                    youporn = upload_video(youporn)
                    send_to_ghost(youporn)
                except Exception as e:
                    print("內層 error ", e)
                    continue
        except Exception as e:
            print("外層 error ", e)
            continue


# # --------------------主要執行----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--yml', help='設置yml位置')
    args = parser.parse_args()

    # 加載環境變量
    Global.load_yaml_file(args.yml)

    youporn_main()
