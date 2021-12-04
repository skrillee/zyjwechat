# !/usr/bin/env python
# coding:utf-8


import socket
import sys


ip_port = ('127.0.0.1', 3368)
sk = socket.socket()
sk.connect(ip_port)

while True:
    inp = input('')
    sk.sendall(inp.encode())

