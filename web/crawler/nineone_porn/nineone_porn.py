import argparse
import uuid
from datetime import datetime

from bs4 import BeautifulSoup
import logging
import asyncio
from urllib.parse import parse_qs, urlparse


# Python 的内置 HTML 解析器
from web.util.download_util import download_m3u8
from web.common.common import check_repeat
from web.db.mypql.db_mysql import insert_data
from web.common.java_api import post_admin_ghostPost_addWithDwLink
from web.common.uploader import upload_file_mega
from web.common.webdriver import call_webdriver
from web.config.yaml_config import Global
from web.do.article_DO import Article_DO
from web.vo.add_with_dw_link_VO import Add_with_dw_link_VO

features = 'html.parser'
# 上傳的路徑
upload_file_path = '/nineone_porn'

source = 'nineone_porn'


class NineOnePorn:
    def __init__(self, view_key, title, video_page_url, tags):
        self.view_key = view_key
        self.video_page_url = video_page_url
        self.title = title
        self.tags = tags
        self.video_upload_url = None
        self.video_local_path = None
        self.file_name = None
        self.file_size = 0
        self.upload_start_time = 0
        self.upload_end_time = 0
        self.download_start_time = 0
        self.download_end_time = 0
        self.md5 = ''

    def set_video_upload_url(self, video_upload_url):
        self.video_upload_url = video_upload_url

    def set_video_local_path(self, video_local_path):
        self.video_local_path = video_local_path

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
        return self.view_key

    def get_title(self):
        return self.title

    def get_video_url(self):
        return self.video_page_url

    def get_video_upload_url(self):
        return self.video_upload_url

    def get_video_local_path(self):
        return self.video_local_path

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
    nine_one_porn_list = []

    page_source = call_webdriver(main_page_url)
    soup = BeautifulSoup(page_source, features)
    for item in soup\
            .select('#wrapper '
                    '.container.container-minheight '
                    '.row '
                    '.col-sm-12 '
                    '.row '
                    '.col-xs-12.col-sm-4.col-md-3.col-lg-3 '
                    '.well.well-sm.videos-text-align '
                    'a'):
        href = item.get('href')
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        video_page_url = href
        view_key = query_params.get('viewkey')[0] if 'viewkey' in query_params else None
        title = item.select_one('.video-title.title-truncate.m-t-5').text
        nine_one_porn = NineOnePorn(view_key, title, video_page_url, tags)

        nine_one_porn_list.append(nine_one_porn)

    return nine_one_porn_list


def video_page(nine_one_porn):
    page_source = call_webdriver(nine_one_porn.get_video_url())

    soup = BeautifulSoup(page_source, features)
    video_soup = soup.select_one('#wrapper '
                                 '.container.container-minheight '
                                 '.row '
                                 '.col-md-8.col-ms-8.col-xs-12.video-border '
                                 '#videodetails '
                                 '.video-container '
                                 '#player_one '
                                 '#player_one_html5_api '
                                 'source')
    if 'src' in video_soup.attrs:
        video_url = video_soup.attrs['src']
        video_name = nine_one_porn.get_view_key()

        mp4_dir = Global.yml_data['nineone_porn']['mp4_dir']
        tmp_dir = Global.yml_data['nineone_porn']['tmp_dir']
        download_rep = download_m3u8(video_url, mp4_dir, tmp_dir, video_name)
        if download_rep is None:
            raise Exception('下載失敗')
        file_name = download_rep.file_name
        video_path = download_rep.folder_path
        file_size = download_rep.size
        download_start_time = download_rep.download_start_time
        download_end_time = download_rep.download_end_time
        md5 = download_rep.md5

        nine_one_porn.set_video_local_path(video_path)
        nine_one_porn.set_file_name(file_name)
        nine_one_porn.set_file_size(file_size)
        nine_one_porn.set_download_start_time(download_start_time)
        nine_one_porn.set_download_end_time(download_end_time)
        nine_one_porn.set_md5(md5)
    return nine_one_porn


def upload_video(nine_one_porn):
    upload_rep = asyncio.run(upload_file_mega(nine_one_porn.video_local_path, upload_file_path))
    video_upload_url = upload_rep.link
    nine_one_porn.set_video_upload_url(video_upload_url)
    return nine_one_porn


def send_to_ghost(nine_one_porn):
    do = Article_DO(id=str(uuid.uuid4()),
                    source=source,
                    article_id=nine_one_porn.get_view_key(),
                    title=nine_one_porn.get_title(),
                    tags=None,
                    content='hello',
                    images=None,
                    source_url=nine_one_porn.get_video_url(),
                    download_url=nine_one_porn.get_video_upload_url(),
                    folder_path=nine_one_porn.get_video_local_path(),
                    status=1,
                    memo=None,
                    update_time=datetime.now(),
                    create_time=datetime.now())
    insert_data(do)

    request = Add_with_dw_link_VO(source=source,
                                  article_id=nine_one_porn.get_view_key(),
                                  title=nine_one_porn.get_title(),
                                  file_name=nine_one_porn.get_file_name(),
                                  content='hello',
                                  tags=None,
                                  source_url=nine_one_porn.get_video_url(),
                                  dwLink=nine_one_porn.get_video_upload_url(),
                                  provider='mega',
                                  file_size=nine_one_porn.get_file_size(),
                                  upload_start_time=nine_one_porn.get_upload_start_time(),
                                  upload_end_time=nine_one_porn.get_upload_end_time(),
                                  download_start_time=nine_one_porn.get_download_start_time(),
                                  download_end_time=nine_one_porn.get_download_end_time(),
                                  md5=nine_one_porn.get_md5())
    post_admin_ghostPost_addWithDwLink(request)


def nineone_porn_main():
    logging.info("91 porn啟動")

    for page in range(1, 99):
        try:
            nine_one_porn_list = main_page('https://91porn.com/v.php?category=ori&viewtype=basic&page=' + str(page),
                                           ['91原創'])
            for nine_one_porn in nine_one_porn_list:
                if check_repeat(source, nine_one_porn.view_key):
                    print(source + '_' + nine_one_porn.view_key + '已經下載過')
                    continue
                try:
                    nine_one_porn = video_page(nine_one_porn)
                    nine_one_porn = upload_video(nine_one_porn)
                    send_to_ghost(nine_one_porn)
                except Exception as e:
                    print("內層 error ", e)
                    continue
        except Exception as e:
            print("外層 error ", e)
            continue


# # --------------------主要執行----------
if __name__ == "__main__":
    logging.info("啟動")

    parser = argparse.ArgumentParser()
    parser.add_argument('--yml', help='設置yml位置')
    args = parser.parse_args()
    # 加載環境變量
    Global.load_yaml_file(args.yml)

    nineone_porn_main()
