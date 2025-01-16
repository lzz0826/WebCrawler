import argparse

from web.crawler.youporn.youporn import youporn_main
from web.crawler.spank_bang.spank_bang import spank_bang_main
from web.config.yaml_config import Global
import logging
from web.config.logging_config import configure_logging
from web.crawler.t66y.t66y import t66y_main
from web.crawler.xnxx.xnxx import xnxx_main
from web.crawler.xvideo.xvideo import xvideo_main
from web.crawler.pornhub.pornhub import pornhub_main
from web.crawler.nineone_porn.nineone_porn import nineone_porn_main

if __name__ == '__main__':
    configure_logging()
    logging.info("主線程啟動")
    parser = argparse.ArgumentParser()
    # python main.py --yml /path/to/your/crawler.yaml 启动指令
    parser.add_argument('--yml', help='設置yml位置', default='/Users/sai/PycharmProjects/WebCrawler/web/crawler.yaml')  # 添加默认值
    args = parser.parse_args()
    # 加載環境變量
    Global.load_yaml_file(args.yml)


    pornhub = Global.yml_data['pornhub']['open']
    if pornhub:
        pornhub_main()
    xvideo = Global.yml_data['xvideo']['open']
    if xvideo:
        xvideo_main()
    spank_bang = Global.yml_data['spank_bang']['open']
    if spank_bang:
        spank_bang_main()
    t66y = Global.yml_data['t66y']['open']
    if t66y:
        t66y_main()
    nineone_porn = Global.yml_data['nineone_porn']['open']
    if nineone_porn:
        nineone_porn_main()
    youporn = Global.yml_data['youporn']['open']
    if youporn:
        youporn_main()
    xnxx = Global.yml_data['xnxx']['open']
    if xnxx:
        xnxx_main()

