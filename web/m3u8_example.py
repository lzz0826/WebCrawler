import m3u8_To_MP4

if __name__ == '__main__':
    m3u8_url = 'https://cv-h.phncdn.com/hls/videos/202305/26/432337041/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_432337041.mp4.urlset/master.m3u8?fhEFbDygSg7Nhdb2foXEaIXISyUL3Iac46YrUTWSl-t_x3tSUVZBGOl4Ve89UvMtYTD3dyz0p7ZZsNu_K68Pdgvlt6rhxKVyRFgfL-jrn1cA3PxUnhm0DmCE6Wo4ORyxny6vs8joLeM9Y0t09CWcKOqYyCJdX9MjDbNs610DnTofn7vy5P0lQ97ih6ZzrcoYHlId_nduv7A'
    mp4_file_dir = '/Users/sai/Desktop/testmp4/ff3'  # 最終mp4的路徑，需要絕對路徑，以免報錯
    tmpdir = '/Users/sai/Desktop/testmp4'  # ts檔的暫存地址
    mp4_file_name = 'test'  # 最終mp4的文件名，生成出來會是test.mp4

    # 1. Download videos from uri.
    m3u8_To_MP4.multithread_download(m3u8_url,
                                     mp4_file_dir=mp4_file_dir,
                                     tmpdir=tmpdir,
                                     mp4_file_name=mp4_file_name)
