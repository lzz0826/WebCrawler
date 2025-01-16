import asyncio
import logging
import os

from mega import Mega
from mega.errors import RequestError
from os.path import basename
from web.common.common import get_current_timestamp
import dropbox
from web.config.yaml_config import Global
from pcloud import PyCloud

mega = Mega()


"""
上傳檔案
"""


class UploadRep:
    def __init__(self, provider, upload_start_time, upload_end_time, link):
        self.provider = provider
        self.upload_start_time = upload_start_time
        self.upload_end_time = upload_end_time
        self.link = link


async def upload_file_mega(file_path, target_folder):

    # 登錄到Mega帳戶
    email = str(Global.yml_data['uploader']['mega']['email'])
    password = str(Global.yml_data['uploader']['mega']['password'])
    m = mega.login(email, password)

    folder = m.find(target_folder)  # 你可以更換為其他的資料夾
    if folder is None:
        print(f"Folder '{target_folder}' not found on MEGA.")
        return None

    # 檢查檔案是否存在，並且避免覆蓋
    if basename(file_path) in [file['a']['n'] for file in m.get_files_in_node(folder)]:
        print(f"File {basename(file_path)} already exists in the destination.")
        return None

    # 上傳一個檔案
    try:
        upload_start_time = get_current_timestamp()
        file = await asyncio.to_thread(m.upload, file_path, folder[0])
        upload_end_time = get_current_timestamp()
    except RequestError as e:
        print(f"An upload error occurred: {e}")
        return None

    # 獲取檔案的連結
    link = m.get_upload_link(file)

    upload_rep = UploadRep('MEGA', upload_start_time, upload_end_time, link)

    return upload_rep


async def upload_file_dropbox(file_path, destination_path):

    file_name = file_path.split('/')[-1]
    destination_path = destination_path + '/' + file_name
    access_token = str(Global.yml_data['uploader']['dropbox']['access_token'])
    dbx = dropbox.Dropbox(access_token)

    check_exists = check_path_exists_dropbox(dbx,destination_path)

    # 檢查檔案是否存在，並且避免覆蓋
    if check_exists:
        print('已上傳過')
        return None

    with open(file_path, "rb") as f:
        file_data = f.read()

    try:
        upload_start_time = get_current_timestamp()
        response = dbx.files_upload(file_data, destination_path)
        upload_end_time = get_current_timestamp()
        print("File uploaded successfully!")

        link = 'https://www.dropbox.com/home{}?preview='.format(destination_path)+file_name.replace(" ","+")

    except dropbox.exceptions.ApiError as e:
        print("File upload error:", e)
    upload_rep = UploadRep('DROPBOX', upload_start_time, upload_end_time, link)
    return upload_rep


def check_path_exists_dropbox(dbx, path):
    try:
        metadata = dbx.files_get_metadata(path)
        return True
    except dropbox.exceptions.ApiError as e:
        return False


def upload_file_pcloud(file_path, destination_path):
    # 設定 pCloud 的帳戶憑證
    username = str(Global.yml_data['uploader']['pcloud']['email'])
    password = str(Global.yml_data['uploader']['pcloud']['password'])
    endpoint = str(Global.yml_data['uploader']['pcloud']['endpoint'])

    pc = PyCloud(username, password, endpoint=endpoint)

    # 指定要檢查的檔案路徑
    file_name = os.path.basename(file_path)

    # 取得檔案列表
    file_list = pc.listfolder(path=destination_path).get('metadata', {}).get('contents', [])

    # 檢查檔案是否存在
    file_exists = any(file.get('name') == file_name for file in file_list)
    if file_exists:
        print('已上傳過')
        return None

    # 上传文件到 pCloud
    logging.info('pCloud上傳開始')
    upload_start_time = get_current_timestamp()
    upload_result = pc.uploadfile(files=[file_path], path=destination_path)
    upload_end_time = get_current_timestamp()

    # 检查上传是否成功
    if 'metadata' in upload_result:
        file_metadata = upload_result['metadata'][0]

        # 获取文件ID
        file_id = file_metadata['fileid']

        # 使用 file ID 获取下载链接
        link_result = pc.getfilelink(fileid=file_id)
        if 'hosts' in link_result and 'path' in link_result:
            download_url = f"https://{link_result['hosts'][0]}{link_result['path']}"
            print(f'Download URL: {download_url}')

            upload_rep = UploadRep('DROPBOX', upload_start_time, upload_end_time, download_url)
            print('上傳結束')
            return upload_rep
        else:
            print('File upload failed.')
    else:
        print('File upload failed.')
    return None


# 方法選擇器字典
methods = {
    'mega': upload_file_mega,
    'dropbox': upload_file_dropbox
}

def uploader_method_selector(uploader_method, file_path, target_folder):
    if uploader_method in methods:
        method = methods[uploader_method]
        result = asyncio.run(method(file_path, target_folder))
        if result is not None:
            return result
        else:
            print(f"{uploader_method} upload failed.")
    else:
        print("Invalid method selected.")


# if __name__ == '__main__':
#     file_path = "/Users/sai/Desktop/crawler.yaml"
#     destination_path = "/test001/crawler.yaml"
#
#     upload_file_dropbox(file_path, destination_path)

# # 執行程式
 # path = '/Users/sai/PycharmProjects/web_walker9998/web/mp4/Nalgona mamando verga y cogida a cuatro patas/Nalgona mamando verga y cogida a cuatro patas.mp4'  # 檔案地址
 # asyncio.run(upload_file(path, '/spank_bang_seed'))
