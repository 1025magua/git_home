"""
-------------------------------------------------
   File Name:db_utils02
   Author:Lee
   date: 2021/9/22-10:47
-------------------------------------------------
"""

import pymysql
from configparser import ConfigParser
from comms.constants import CONF_FILE


class DBUtils:
    count = -1

    # 封装连接对象和游标对象
    def __init__(self):
        try:
            cf = ConfigParser()
            cf.read(CONF_FILE, encoding='utf-8')
            host = cf.get('mysql', 'host')
            port = cf.getint('mysql', 'port')
            user = cf.get('mysql', 'user')
            passwd = cf.get('mysql', 'password')
            db = cf.get('mysql', 'db')

            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('工具类连接出现异常，请检查DBUtils中的__init__方法')
            print(e)

    # 封装关闭游标和连接对象
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 封装查询结果集有多少条数据:条目数
    # 如果execute()括号里只传一个参数,我们需要运行count = cursor.execute(sql)
    # 如果execute()传2个参数,我们需要运行count = cursor.execute(sql,占位符数据(元组))
    def find_count(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
                return self.count
            elif params is not None:
                self.count = self.cursor.execute(sql, params)
                return self.count
        except Exception as e:
            print('查询数据库条目数失败:', e)

    # 封装增删改
    # 如果execute()括号里只传一个参数,我们需要运行count = cursor.execute(sql)
    # 如果execute()传2个参数,我们需要运行count = cursor.execute(sql,占位符数据(元组))
    def cud(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
            if isinstance(params, tuple):
                self.count = self.cursor.execute(sql, params)
            if isinstance(params, list):
                self.count = self.cursor.executemany(sql, params)
            self.conn.commit()
            return self.count
        except Exception as e:
            print('增删改执行失败:', e)

    # 封装查询一条数据:execute(sql)    execute(sql,params)
    def find_one(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.cursor.execute(sql)  # 执行sql语句，并且把结果存在cursor里
                return self.cursor.fetchone()  # 从结果集获取一条数据
            elif params is not None:
                self.cursor.execute(sql, params)
                return self.cursor.fetchone()
        except Exception as e:
            print('查询单条数据失败:', e)

    # 封装查询所有数据
    def find_all(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            elif params is not None:
                self.cursor.execute(sql, params)
                return self.cursor.fetchall()
        except Exception as e:
            print('查询所有数据失败:', e)


if __name__ == '__main__':
    db = DBUtils()
    one = db.find_one('select * from tb_user ORDER BY rand() limit 1;')
    print(one[1], one[2])
