# !/usr/bin/env python
# coding:utf-8


import socket
import sys


ip_port = ('192.168.10.172', 9000)
sk = socket.socket()
sk.connect(ip_port)

while True:
    inp = input('')
    sk.sendall(inp.encode())