# !/usr/bin/env python
# coding:utf-8


import socket


ip_port = ('47.92.85.245', 3367)
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
