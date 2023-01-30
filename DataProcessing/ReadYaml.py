# coding=utf-8
import os
import yaml
import json,numpy
#读取yml中的文件

proDir =  os.path.abspath(os.path.dirname(__file__))
path=os.path.join(os.path.split(proDir)[0],'GlobalData','data.yml')


class ReadYaml:
    def __init__(self,path,parms=None):
        self.path=path
        self.parms=parms

    def get_data(self,encoding='utf=8'):
        with open(self.path,encoding=encoding) as f:
            data=yaml.load(f.read(),Loader=yaml.FullLoader)

            if self.parms == None:
                return data
            else:
                return data.get(self.parms)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


    def load_json(path):
        with open(path,encoding='utf-8') as f:
            data = json.dumps(f,cls=MyEncoder,indent=4)
        print(data)


if __name__ == '__main__':
    m=ReadYaml(path,).get_data()['db_info']
    print(m)
    # n=MyEncoder().load_json(path)
    # print(n)
