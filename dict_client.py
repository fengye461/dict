"""
dict客户端

功能: 根据用户输入发送请求,得到结果
      一级: 注册 登录 退出
      二级: 查单词 历史记录 注销
"""

from socket import *
import getpass
import sys

# 声明服务器地址
ADDR = ('127.0.0.1',8000)
# 创建tcp套接字
s = socket()
s.connect(ADDR)


# 查单词
def do_query(name):
    while True:
        word = input("单词:")
        if word == '##': # 结束单词查询
            break
        msg = "Q %s %s" % (name,word)
        s.send(msg.encode()) # 发送请求
        # 得到查询结果
        data = s.recv(2048).decode()
        print(data)


# 历史记录
def do_query_hist():
    s.send(b'H')
    data = s.recv(1024)
    print(data.decode())


# 二级界面,登录后的状态
def login(name):
    while True:
        print("""
        ============= Query =============
        1. 查单词   2. 历史记录    3. 注销
        =================================
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_query_hist()
        elif cmd == "3":
            return
        else:
            print("请输入正确选项")


# 注册函数
def do_register():
    while True:
        name = input("User:")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass("Again:")

        if passwd != passwd1:
            print("两次密码不一致!")
            continue
        if ' ' in name or ' ' in passwd:
            print("用户名密码不能有空格")
            continue

        msg = "R %s %s" % (name,passwd)
        s.send(msg.encode()) # 发送给服务器
        data = s.recv(128).decode() # 接收结果
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 登录
def do_login():
    while True:
        name = input("user:")
        pwd = getpass.getpass()
        msg = "L %s %s" % (name,pwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print("登录成功")
            login(name)
        else:
            print("登录失败")
        return


# 搭建网络连接
def main():
    while True:
        print("""
        =============Welcome=============
        1. 注册      2. 登录        3. 退出
        =================================
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")


main() # 启动客户端