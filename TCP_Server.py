# -*- coding: utf-8 -*-
# Copyright (C) 2023 # @version
# @Time    : 2023/6/24 21:21
# @Author  : Oraer
# @File    : TCP_Server.py
import socket

# 明确配置变量
ip_port = ('192.168.51.175', 4004)
back_log = 5
buffer_size = 1024
# 创建一个TCP套接字
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
# 绑定端口号
ser.bind(ip_port)  # 写哪个ip就要运行在哪台机器上
# 设置半连接池
ser.listen(back_log)  # 最多可以连接多少个客户端
print("服务器已经启动，等待客户端连接")
while 1:
    # 阻塞等待，创建连接
    con, address = ser.accept()  # 在这个位置进行等待，监听端口号
    print("客户端的ip地址和端口号为：", address)
    while 1:
        try:
            # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # con.send(now_time.encode('utf-8')
            # 接受套接字的大小，怎么发就怎么收
            msg = con.recv(buffer_size)
            de_msg = msg.decode('utf-8')
            if de_msg == '1' or de_msg == 'exit' or de_msg == 'quit':
                # 断开连接
                con.close()
                break
            print("Re: ", de_msg)
        except Exception as e:
            break
    print("客户端已经断开连接")
    print("-"*30)
    break

# 关闭服务器
ser.close()
