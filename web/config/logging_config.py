import logging


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # 输出到终端
            logging.FileHandler('logfile.log')  # 输出到日志文件
        ]
    )
