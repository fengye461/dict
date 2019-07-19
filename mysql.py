"""
数据库操作模块
思路:
将数据库操作封装为一个类,将dict_server需要的数据库操作功能分别写成方法,
在dict_server中实例化对象,需要什么方法直接调用
"""

import pymysql
import hashlib

SALT = "#&Aid_"  # 盐

class Database:
    def __init__(self,host='localhost',
                 port = 3306,
                 user = 'root',
                 password = '123456',
                 database = None,
                 charset = 'utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_database()  # 连接数据库

    # 连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.password,
                                  database = self.database,
                                  charset = self.charset)

    # 关闭数据库
    def close(self):
        self.db.close()

    # 创建游标
    def create_cur(self):
        self.cur = self.db.cursor()

    def register(self,name,passwd):
        sql = "select * from user where name = '%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 查找到则用户存在
        if r:
            return False

        hash = hashlib.md5((name+SALT).encode())  # 加盐处理
        hash.update(passwd.encode()) # 算法加密
        passwd = hash.hexdigest()  # 加密后的密码

        # 插入数据库
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    # 登录
    def login(self,name,pwd):
        # 密码加密处理
        hash = hashlib.md5((name + SALT).encode())  # 加盐处理
        hash.update(pwd.encode())  # 算法加密
        passwd = hash.hexdigest()  # 加密后的密码

        sql = "select name,passwd from user where name = '%s' and passwd = '%s'" % (name,pwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        return False

    # 插入历史记录
    def insert_his(self,name, word):
        sql = "insert into hist (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    # 查单词
    def query(self,word):
        sql = "select intepret from words where word = '%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 如果找到 r --> (mean,)
        if r:
            return r[0]

    # 历史记录
    def query_hist(self):
        sql = "select * from hist order by time desc limit 10"
        self.cur.execute(sql)
        r = self.cur.fetchall()
        if r:
            return r
