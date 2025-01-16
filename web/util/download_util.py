import m3u8_To_MP4
from web.common.common import get_current_timestamp
import requests
import youtube_dl
import os
import hashlib


class DownloadRep:
    def __init__(self, file_name, folder_path, download_start_time, download_end_time, size, md5):
        self.file_name = file_name
        self.folder_path = folder_path
        self.download_start_time = download_start_time
        self.download_end_time = download_end_time
        self.size = size
        self.md5 = md5


def get_file_size_kb(url, headers):
    try:
        response = requests.head(url, headers=headers, allow_redirects=True)
        if 'Content-Length' in response.headers:
            file_size = bytes_to_KB(int(response.headers['Content-Length']))
            return file_size
        else:
            print('無法獲取檔案大小')
    except Exception as e:
        print('獲取檔案大小時發生錯誤:', str(e))
    return None


def download_mp4(movie_url, mp4_name, save_directory, headers, set_file_size_mb):
    file_name = mp4_name + '.mp4'
    if not (mp4_name and save_directory and headers):
        print("download_mp4缺少必要的參數")
        return None
    try:
        file_size = get_file_size_kb(movie_url, headers)
        if file_size is None:
            print('取得不到檔案大小')
            return None
        if file_size >= set_file_size_mb:
            print('檔案太大')
            return None
        folder_path = os.path.join(save_directory, mp4_name)
        os.makedirs(folder_path, exist_ok=True)
        save_path = os.path.join(folder_path, file_name)
        downsize = 0
        print('開始下載: ' + movie_url)
        download_start_time = get_current_timestamp()
        req = requests.get(movie_url, headers=headers, stream=True, verify=False)
        with open(save_path, 'wb') as f:
            for chunk in req.iter_content(chunk_size=10000):
                if chunk:
                    f.write(chunk)
                    downsize += len(chunk)
                    line = 'downloading %.2f%% - %.2f MB， 共 %.2f MB'
                    line = line % (downsize / (file_size*1024) * 100, downsize / 1024 / 1024, file_size / 1024)
                    print(line)
        download_end_time = get_current_timestamp()
        md5 = calculate_md5(save_path)
        download_rep = DownloadRep(file_name, folder_path, download_start_time, download_end_time, file_size,md5)
        return download_rep
    except Exception as e:
        print('下載MP4時發生錯誤:', str(e))
    return None


def download_yt(urls, proxy, mp4_file_dir, mp4_file_name):
    file_name = mp4_file_name + '.mp4'
    download_start_time = get_current_timestamp()
    ydl_opts = {'ignoreerrors': True,
                'outtmpl': os.path.join(mp4_file_dir, mp4_file_name + '.%(ext)s'),
                'proxy': proxy}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    download_end_time = get_current_timestamp()
    video_path = os.path.join(mp4_file_dir, file_name)
    file_size = bytes_to_KB(os.path.getsize(video_path))
    md5 = calculate_md5(video_path)
    download_rep = DownloadRep(file_name, video_path, download_start_time, download_end_time, file_size,md5)
    return download_rep


def download_m3u8(m3u8_url, mp4_file_dir, tmpdir, mp4_file_name):
    file_name = mp4_file_name + '.mp4'
    os.makedirs(mp4_file_dir, exist_ok=True)
    os.makedirs(tmpdir, exist_ok=True)
    download_start_time = get_current_timestamp()
    m3u8_To_MP4.multithread_download(m3u8_url,
                                     mp4_file_dir=mp4_file_dir,
                                     tmpdir=tmpdir,
                                     mp4_file_name=mp4_file_name)
    video_path = os.path.join(mp4_file_dir, file_name)
    download_end_time = get_current_timestamp()
    file_size = bytes_to_KB(os.path.getsize(video_path))
    md5 = calculate_md5(video_path)
    download_rep = DownloadRep(file_name, video_path, download_start_time, download_end_time, file_size,md5)
    return download_rep


def calculate_md5(file_path):
    try:
        with open(file_path, 'rb') as f:
            md5_hash = hashlib.md5()
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        print('计算 MD5 值时发生错误:', str(e))
    return None


def bytes_to_KB(file_size):
    return file_size // 1024

