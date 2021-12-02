#!/usr/bin/env python
# coding:utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zyjwechat.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import socketserver
import json
from wechat import models


class MyServer(socketserver.BaseRequestHandler):
    def __init__(self, request: '', client_address: '', server: ''):
        self.methanal_value = ''
        self.number = ''
        self.time = []
        super().__init__(request, client_address, server)

    def setup(self):
        pass

    def handle(self):
        conn = self.request
        try:
            while True:
                receive_data_encode = conn.recv(6144)
                receive_data_decode = receive_data_encode.decode()
                if receive_data_decode:
                    receive_data_json = json.loads(receive_data_decode)
                    if receive_data_json['value'] == 'close':
                        models.Methanal.objects.create(number=self.number, time=self.time,
                                                       methanal_value=self.methanal_value)
                        conn.close()
                    else:
                        self.methanal_value += receive_data_json['value']
                        time = receive_data_json['time']
                        self.time.append(time)
                        self.number = receive_data_json['number']

        except OSError as e:
            pass

    def finish(self):
        pass


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('47.92.85.245', 1883), MyServer)
    server.serve_forever()
