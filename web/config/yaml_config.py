import os

import yaml

class Global:
    yml_data = None
    @staticmethod
    def load_yaml_file(file_path):
        with open(file_path, 'r') as file:
            Global.yml_data = yaml.load(file, Loader=yaml.FullLoader)

    # @staticmethod
    # def load_yaml_file(file_name='crawler.yaml'):
    #     # 获取当前文件的绝对路径，并推导项目根目录
    #     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #     file_path = os.path.join(base_dir, 'WebCrawler', 'web', file_name)
    #
    #     # 加载 YAML 文件
    #     with open(file_path, 'r') as file:
    #         Global.yml_data = yaml.load(file, Loader=yaml.FullLoader)
