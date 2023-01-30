# coding=utf-8
#通过读取数据库提取测试元素
import json
import pymysql,os
from DataProcessing.ReadYaml import ReadYaml
from Log.logger import log
proDir =  os.path.abspath(os.path.dirname(__file__))
path=os.path.join(os.path.split(proDir)[0],'GlobalData','data.yml')


class Read_DB:
    def __init__(self):
        m=ReadYaml(path, 'db_info').get_data()
        self.config = {
            'host': m['host'],
            'user': m['user'],
            'passwd': m['pwd'],
            'port': m['port'],
            'db': m['dbname']
        }

    def connectDB(self):
        try:
            # connect to DB
            self.db = pymysql.connect(**self.config)
            # create cursor
            self.cursor = self.db.cursor()
            log.info("Connect DB successfully!")
        except ConnectionError as ex:
            log.info("连接数据库失败")
        return self.db

    def executeSQL(self, sql,args=None,one=True):
        self.connectDB()
        try:
            self.cursor.execute(sql,args)
            self.db.commit()
            if one:
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            log.info(str(e))

    def commit_data(self, sql):
        """
        提交数据(更新、插入、删除操作)
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交事务
            self.db.commit()
        except:
            # 若出现错误，则回滚
            self.db.rollback()

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    r=Read_DB()
    x=r.executeSQL("select * from interfacetestplatform_testcase")
    t=json.loads(x[2])
    print(t['user_id'])


