#!/usr/bin/env python
# coding:utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zyjwechat.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import socketserver
import json
from wechat import models
# from django.shortcuts import HttpResponse
# from rest_framework.views import APIView


class MyServer(socketserver.BaseRequestHandler):
    def __init__(self, request: '', client_address: '', server: ''):
        super().__init__(request, client_address, server)

    def setup(self):
        pass

    def handle(self):
        conn = self.request
        address_ip = self.client_address[0]
        address_port = self.client_address[1]
        methanal_value = ''
        time = ''
        try:
            while True:
                self.request.settimeout(5)
                receive_data_encode = conn.recv(6144)
                receive_data_decode = receive_data_encode.decode()
                if receive_data_decode:
                    receive_data_json = json.loads(receive_data_decode)
                    number = receive_data_json['number']
                    if receive_data_json['value'] == 'close':
                        invitation_code = models.Equipment.objects.filter(number=number).first().invitation_code
                        models.Methanal.objects.create(number=number, time=time, invitation_code=invitation_code,
                                                       methanal_value=methanal_value, ip=address_ip, port=address_port)
                        conn.close()
                    elif receive_data_json['value'] == 'start':
                        client_address_ip = receive_data_json['address_ip']
                        client_address_port = receive_data_json['address_port']
                        self.request.sendto('start'.encode(), (client_address_ip, int(client_address_port)))
                    elif receive_data_json['value'] == 'bind':
                        models.Equipment.objects.update_or_create(
                            defaults={'port': address_port, 'ip': address_ip},
                            number=number)
                    else:
                        methanal_value += receive_data_json['value'] + ','
                        time += receive_data_json['time'] + ','
        except OSError as e:
            pass

    def finish(self):
        pass


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 3367), MyServer)
    server.serve_forever()
