import argparse
import logging
import uuid
from datetime import datetime
import os


import requests
import re
from bs4 import BeautifulSoup

from web.common.webdriver import call_webdriver
from web.util.download_util import download_mp4
from web.common.common import check_repeat

# url前綴
from web.db.mypql.db_mysql import insert_data
from web.common.java_api import post_admin_ghostPost_addWithDwLink
from web.common.uploader import uploader_method_selector
from web.do.article_DO import Article_DO
from web.vo.add_with_dw_link_VO import Add_with_dw_link_VO
from web.config.yaml_config import Global

url_prefix = 'https://www.xnxx.com'

# Python 的内置 HTML 解析器
features = 'html.parser'

source = 'xnxx'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}



class Xnxx:
    def __init__(self, video_id, title, video_page_url, tags):
        self.video_id = video_id
        self.video_page_url = video_page_url
        self.title = title
        self.tags = tags
        self.video_upload_url = None
        self.video_local_folder = None
        self.file_name = None
        self.provider = ''
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

    def set_provider(self, provider):
        self.provider = provider

    def get_view_key(self):
        return self.video_id

    def get_provider(self):
        return self.provider

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

    xnxx_list = []

    res = requests.get(main_page_url, proxies=None)
    soup = BeautifulSoup(res.text, features=features)
    for item in soup \
            .select('#content-thumbs '
                    '.mozaique.cust-nb-cols '
                    'div'):

        video_id = item.get('id')
        if video_id is None:
            continue
        a = item.select_one('div.thumb-under '
                            'a')

        href = a.get('href')
        video_url = url_prefix + href
        title = a.get('title')


        xnxx_one = Xnxx(video_id, title, video_url, tags)
        xnxx_list.append(xnxx_one)

    return xnxx_list

def video_page(xnxx_one,set_file_size_mb):
    html_content = call_webdriver(str(xnxx_one.get_video_page_url()))
    # 使用正則表達式從 <script> 標籤中找到 M3U8 URL
    mp4_url = re.search(r'html5player.setVideoUrlHigh\(\'.*\'\);', html_content)

    if mp4_url:
        mp4_url = mp4_url.group(0)
        mp4_url = mp4_url.replace("html5player.setVideoUrlHigh(\'", "")
        mp4_url = mp4_url.replace("\');", "")

        current_directory = str(Global.yml_data['xnxx']['current_directory'])
        download_rep = download_mp4(mp4_url, xnxx_one.get_title(), current_directory, headers, set_file_size_mb)
        if download_rep is None:
            raise Exception('下載失敗')
        file_name = download_rep.file_name
        video_path = download_rep.folder_path
        file_size = download_rep.size
        download_start_time = download_rep.download_start_time
        download_end_time = download_rep.download_end_time
        md5 = download_rep.md5

        xnxx_one.set_video_local_folder(video_path)
        xnxx_one.set_file_name(file_name)
        xnxx_one.set_file_size(file_size)
        xnxx_one.set_download_start_time(download_start_time)
        xnxx_one.set_download_end_time(download_end_time)
        xnxx_one.set_md5(md5)
    else:
        raise Exception('未找到符合的內容')

    return xnxx_one


def upload_video(xnxx_one):
    video_path = os.path.join(xnxx_one.video_local_folder, xnxx_one.get_title() + '.mp4')

    upload_file_path = str(Global.yml_data['xnxx']['upload_file_path'])
    upload_space_name = str(Global.yml_data['xnxx']['upload_space_name'])
    upload_rep = uploader_method_selector(upload_space_name, video_path, upload_file_path)

    video_upload_url = upload_rep.link
    provider = upload_rep.provider
    upload_start_time = upload_rep.upload_start_time
    upload_end_time = upload_rep.upload_end_time

    xnxx_one.set_video_upload_url(video_upload_url)
    xnxx_one.set_upload_start_time(upload_start_time)
    xnxx_one.set_upload_end_time(upload_end_time)
    xnxx_one.set_provider(provider)


    return xnxx_one


def send_to_ghost(xnxx_one):
    do = Article_DO(id=str(uuid.uuid4()),
                    source=source,
                    article_id=xnxx_one.get_view_key(),
                    title=xnxx_one.get_title(),
                    tags=None,
                    content='hello',
                    images=None,
                    source_url=xnxx_one.get_video_page_url(),
                    download_url=xnxx_one.get_video_upload_url(),
                    folder_path=xnxx_one.get_video_local_folder(),
                    status=1,
                    memo=None,
                    update_time=datetime.now(),
                    create_time=datetime.now())
    insert_data(do)

    request = Add_with_dw_link_VO(source=source,
                                  article_id=xnxx_one.get_view_key(),
                                  title=xnxx_one.get_title(),
                                  file_name=xnxx_one.get_file_name(),
                                  content='hello',
                                  tags=None,
                                  source_url=xnxx_one.get_video_page_url(),
                                  dwLink=xnxx_one.get_video_upload_url(),
                                  provider=xnxx_one.get_provider(),
                                  file_size=xnxx_one.get_file_size(),
                                  upload_start_time=xnxx_one.get_upload_start_time(),
                                  upload_end_time=xnxx_one.get_upload_end_time(),
                                  download_start_time=xnxx_one.get_download_start_time(),
                                  download_end_time=xnxx_one.get_download_end_time(),
                                  md5=xnxx_one.get_md5())
    post_admin_ghostPost_addWithDwLink(request)


def xnxx_main():
    logging.info("XNXX啟動")
    # 設定檔案大小設定(MB)
    set_file_size_mb = int(Global.yml_data['xnxx']['set_file_size_mb'])

    for page in range(1, 99):
        try:
            xvideo_list = main_page('https://www.xnxx.com/search/asian_woman' + str(page), ['亞洲'])
            for xvideo in xvideo_list:
                if check_repeat(source, xvideo.video_id):
                    print(source + '_' + xvideo.video_id + '已經下載過')
                    continue
                try:
                    xvideo = video_page(xvideo, set_file_size_mb)
                    xvideo = upload_video(xvideo)
                    send_to_ghost(xvideo)
                except Exception as e:
                    print("內層 error ", e)
                    continue
        except Exception as e:
            print("外層 error ", e)
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--yml', help='設置yml位置')
    args = parser.parse_args()

    # 加載環境變量
    Global.load_yaml_file(args.yml)

    xnxx_main()
