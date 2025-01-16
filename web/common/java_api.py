import requests
import time
from web.config.logging_config import configure_logging
from web.config.yaml_config import Global

configure_logging()


# MP4
def post_admin_ghostPost_addWithDwLink(vo):

    try:
        add_with_dw_link = Global.yml_data['java_api_url']['post']['addWithDwLink']
        url = str(add_with_dw_link)
        payload = {
            'articleId': vo.article_id,
            'title': vo.title,
            'content': vo.content,
            'fileName': vo.file_name,
            'tags': vo.tags,
            'provider': vo.provider,
            'fileSize': vo.file_size,
            'source': vo.source,
            'sourceUrl': vo.source_url,
            'dwLink': vo.dwLink,
            'uploadStartTime': vo.upload_start_time,
            'uploadEndTime': vo.upload_end_time,
            'downloadStartTime': vo.download_start_time,
            'downloadEndTime': vo.download_end_time,
            'md5': vo.md5
            }
        files = []
        headers = {
            'Authorization': 'jwtTokenTest'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.text)
    except Exception as e:
        print("post_admin_ghostPost_add error:", e.with_traceback())
        return None

# ˊ種子
def post_admin_ghostPost_addWithTorrent(vo):
    try:
        add_with_torrent = Global.yml_data['java_api_url']['post']['addWithTorrent']
        url = str(add_with_torrent)
        payload = {'articleId': vo.article_id,
                   'title': vo.title,
                   'content': vo.content,
                   'tags': vo.tags,
                   'source': vo.source,
                   'sourceUrl': vo.source_url}

        path = vo.folder_path + '/' + vo.file_name + '.torrent'

        files = [
            ('file', (vo.file_name, open(path, 'rb'), 'application/octet-stream'))
        ]
        headers = {
            'Authorization': 'jwtTokenTest'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_data = response.json()  # 解析JSON数据
        status_code = json_data.get('statusCode')
        if status_code == -1:
            time.sleep(5)
        print(response.text)

    except Exception as e:
        print("post_admin_ghostPost_add error ", e.with_traceback())
        return None


def isPostExisted(source, articleId):
    try:
        is_post_existed = Global.yml_data['java_api_url']['get']['isPostExisted']
        url = str(is_post_existed).format(articleId,source)
        payload = {}
        headers = {
            'Authorization': 'jwtTokenTest'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        json_res = response.json()

        return bool(json_res['data'])


    except Exception as e:
        print("post_admin_ghostPost_add error ", e.with_traceback())
        return None
