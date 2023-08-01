# -*- coding: utf-8 -*-
# Copyright (C) 2023 # @version
# @Time    : 2023/6/24 21:22
# @Author  : Oraer
# @File    : TCP_Client.py
import socket
import sys


def tcp_client():
    IP = '192.168.51.175'   # 服务器的ip地址
    port = 4004              # 服务器的端口号
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP, port))
    except Exception as e:
        print('server not find or not open')
        sys.exit()
    while 1:
        msg = input('please input:')
        # 防止输入空消息
        if not msg:
            continue
        s.send(msg.encode('utf-8'))  # 收发消息一定要二进制，记得编码
        if msg == '1' or msg == 'exit' or msg == 'quit':
            s.close()
            break
    s.close()

if __name__ == '__main__':
    tcp_client()
