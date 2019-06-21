"""
读取配置。这里配置文件用的yaml，也可用其他如XML,INI等，需在file_reader中添加相应的Reader进行处理。
"""
import os
from utils.file_reader import YamlReader

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
POM_PATH = os.path.join(BASE_PATH, 'pom')
DOCS_PATH = os.path.join(BASE_PATH, 'docs')


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)


if __name__ == '__main__':
    # 实例化对象
    c = Config()
    # 输出config.yml 文件中URL字段
    print(c.get('URL'))
    # 输出自动化项目基础目录，后面所有跟目录相关的，都跟此目录联系在一起
    print(BASE_PATH)
    # 输出日志格式
    pattern = c.get('log')
    print(pattern['pattern'])
    # 输出报告目录
    print(REPORT_PATH)