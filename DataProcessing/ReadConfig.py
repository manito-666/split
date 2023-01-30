# coding=utf-8
#通过configparser读取config.ini文件
import configparser,os
from Log.logger import log
proDir =  os.path.abspath(os.path.dirname(__file__))
path=os.path.join(os.path.split(proDir)[0],'ConfigFile','config.ini')
#初始化实例

class ReadConfig:
    def __init__(self,filename,encoding='utf-8'):
        self.filename=filename
        self.encoding=encoding
        self.conf=configparser.ConfigParser()
        self.conf.read(filename, encoding)

    def get_str(self,section,option):

        return self.conf.get(section,option)

    def get_int(self, section, option):
        return self.conf.getint(section, option)

    def get_float(self, section, option):
        pass

    def get_bool(self, section, option):
        pass

    def write_data(self, section, option, value):
        pass

if __name__ == '__main__':
    m=ReadConfig(path).get_str('http','url')
    print(m)