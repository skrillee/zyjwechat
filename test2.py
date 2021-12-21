# !/usr/bin/env python
# coding:utf-8


import socket


ip_port = ('127.0.0.1', 3367)
sk = socket.socket()
sk.connect(ip_port)

while True:

    inp = input('')
    sk.sendall(inp.encode())
    data = sk.recv(1024)
    print(data)

    if inp == 'exit':
        break
sk.close()
