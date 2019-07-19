"""
二级界面
"""
def fun():
    while True:
        print("********二级界面********")

        cmd = input("二级命令:")
        if cmd == '其他命令':
            pass
        elif cmd == '注销':
            break

while True:
    print("***********一级界面**********")

    cmd = input("一级命令:")

    if cmd == '登录':
        fun()

    elif cmd == '注册':
        fun()

    elif cmd == '退出':
        break
