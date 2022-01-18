# !/usr/bin/env python
# coding:utf-8


import socket

ip_port = ('47.92.85.245', 3367)
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
