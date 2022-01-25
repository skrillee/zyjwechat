# !/usr/bin/env python
# coding:utf-8


import socket

ip_port = ('127.0.0.1', 3367)
sk = socket.socket()
sk.connect(ip_port)
inp = input('')
sk.sendall(inp.encode())
inp = input('')
sk.sendall(inp.encode())
while True:
    data = sk.recv(1024)
    print(data)

    # if inp == 'exit':
    #     break
# sk.close()
