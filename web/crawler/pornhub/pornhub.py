import asyncio
import logging
import uuid
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from web.util.download_util import download_yt
from web.common.common import check_repeat


# url前綴
from web.db.mypql.db_mysql import insert_data
from web.common.java_api import post_admin_ghostPost_addWithDwLink
from web.common.uploader import upload_file_mega
from web.do.article_DO import Article_DO
from web.vo.add_with_dw_link_VO import Add_with_dw_link_VO
from web.config.yaml_config import Global

url_prefix = 'https://cn.pornhub.com'
# Python 的内置 HTML 解析器
features = 'html.parser'
upload_file_path = '/pornhub'

source = 'pornhub'


class PornHub:
    def __init__(self, view_key, title, video_url, tags):
        self.view_key = view_key
        self.title = title
        self.video_url = video_url
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
        return self.video_url

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
    porn_hub_list = []

    res = requests.get(main_page_url, proxies=None)
    soup = BeautifulSoup(res.text, features=features)
    for item in soup\
            .select('#videoCategory '
                    '.pcVideoListItem.js-pop.videoblock.videoBox '
                    'div.wrap div.thumbnail-info-wrapper.clearfix '
                    'span.title '
                    'a'):
        href = item.get('href')
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        video_url = url_prefix + href
        view_key = query_params.get('viewkey')[0] if 'viewkey' in query_params else None
        title = item.get('title')
        porn_hub = PornHub(view_key, title, video_url, tags)

        porn_hub_list.append(porn_hub)

    return porn_hub_list


def video_page(pornhub):
    urls = [pornhub.get_video_url()]
    proxy = ''
    video_name = pornhub.view_key

    mp4_dir = Global.yml_data['pornhub']['mp4_dir']

    download_rep = download_yt(urls=urls, proxy=proxy, mp4_file_dir=mp4_dir, mp4_file_name=video_name)
    if download_rep is None:
        raise Exception('下載失敗')

    video_path = download_rep.folder_path
    file_name = download_rep.file_name
    file_size = download_rep.size
    download_start_time = download_rep.download_start_time
    download_end_time = download_rep.download_end_time
    md5 = download_rep.md5

    pornhub.set_video_local_path(video_path)
    pornhub.set_file_name(file_name)
    pornhub.set_file_size(file_size)
    pornhub.set_download_start_time(download_start_time)
    pornhub.set_download_end_time(download_end_time)
    pornhub.set_md5(md5)

    return pornhub


def upload_video(pornhub):
    upload_rep = asyncio.run(upload_file_mega(pornhub.video_local_path, upload_file_path))
    video_upload_url = upload_rep.link
    upload_start_time = upload_rep.upload_start_time
    upload_end_time = upload_rep.upload_end_time

    pornhub.set_video_upload_url(video_upload_url)
    pornhub.set_upload_start_time(upload_start_time)
    pornhub.set_upload_end_time(upload_end_time)
    return pornhub


def send_to_ghost(pornhub):
    do = Article_DO(id=str(uuid.uuid4()),
                    source=source,
                    article_id=pornhub.get_view_key(),
                    title=pornhub.get_title(),
                    tags=None,
                    content='hello',
                    images=None,
                    source_url=pornhub.get_video_url(),
                    download_url=pornhub.get_video_upload_url(),
                    folder_path=pornhub.get_video_local_path(),
                    status=1,
                    memo=None,
                    update_time=datetime.now(),
                    create_time=datetime.now())
    insert_data(do)

    request = Add_with_dw_link_VO(source=source,
                                  article_id=pornhub.get_view_key(),
                                  title=pornhub.get_title(),
                                  file_name=pornhub.get_file_name(),
                                  content='hello',
                                  tags=None,
                                  source_url=pornhub.get_video_url(),
                                  dwLink=pornhub.get_video_upload_url(),
                                  provider='mega',
                                  file_size=pornhub.get_file_size(),
                                  upload_start_time=pornhub.get_upload_start_time(),
                                  upload_end_time=pornhub.get_upload_end_time(),
                                  download_start_time=pornhub.get_download_start_time(),
                                  download_end_time=pornhub.get_download_end_time(),
                                  md5=pornhub.get_md5())
    post_admin_ghostPost_addWithDwLink(request)


# # --------------------主要執行----------
def pornhub_main():
    logging.info("PornHub啟動")

    for page in range(1, 99):
        try:
            porn_hub_list = main_page('https://cn.pornhub.com/video?c=17&page=' + str(page), ['黑人女'])
            for pornhub in porn_hub_list:
                if check_repeat(source, pornhub.view_key):
                    print(source + '_' + pornhub.view_key + '已經下載過')
                    continue
                try:
                    pornhub = video_page(pornhub)
                    pornhub = upload_video(pornhub)
                    send_to_ghost(pornhub)
                except Exception as e:
                    print("內層 error ", e)
                    continue
        except Exception as e:
            print("外層 error ", e)
            continue


if __name__ == "__main__":
    pornhub_main()
