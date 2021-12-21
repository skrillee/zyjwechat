#!/usr/bin/env python
# coding:utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zyjwechat.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import socketserver
import json
from wechat import models
import time
import datetime
# from django.shortcuts import HttpResponse
# from rest_framework.views import APIView
socket_hashMap = {}


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
        times = ''
        try:
            flag = True
            while flag:
                receive_data_encode = conn.recv(6144)
                receive_data_decode = receive_data_encode.decode()
                if receive_data_decode:
                    receive_data_json = json.loads(receive_data_decode)
                    number = receive_data_json['number']
                    if receive_data_json['value'] == 'close':
                        invitation_code = models.Equipment.objects.filter(number=number).first().invitation_code
                        models.Methanal.objects.create(number=number, time=times, invitation_code=invitation_code,
                                                       methanal_value=methanal_value, ip=address_ip, port=address_port)
                        conn.close()
                        flag = False
                    elif 'wifi' in receive_data_json['value']:
                        local_time = datetime.datetime.now()
                        local_time_month = str(local_time.month)
                        local_time_day = str(local_time.day)
                        local_time_hour = str(local_time.hour+8)
                        local_time_minute = str(local_time.minute)
                        local_time_result = local_time_month + '-' + local_time_day + '-' + local_time_hour + ':' + local_time_minute
                        receive_number = receive_data_json['number']
                        hash_map_request = socket_hashMap[receive_number]
                        wifi_data = receive_data_json['value']
                        hash_map_request.send((wifi_data+',' + local_time_result).encode(),)
                        conn.close()
                        time.sleep(610)
                        flag = False
                    elif receive_data_json['value'] == 'start':
                        # client_address_ip = receive_data_json['address_ip']
                        # client_address_port = receive_data_json['address_port']
                        local_time = datetime.datetime.now()
                        local_time_month = str(local_time.month)
                        local_time_day = str(local_time.day)
                        local_time_hour = str(local_time.hour+8)
                        local_time_minute = str(local_time.minute)
                        local_time_result = local_time_month + '-' + local_time_day + '-' + local_time_hour + ':' + local_time_minute
                        receive_number = receive_data_json['number']
                        hash_map_request = socket_hashMap[receive_number]
                        hash_map_request.send(('start,' + local_time_result).encode(),)
                        conn.close()
                        time.sleep(610)
                        flag = False
                    elif receive_data_json['value'] == 'bind':
                        models.Equipment.objects.update_or_create(
                            defaults={'port': address_port, 'ip': address_ip},
                            number=number)
                        receive_number = receive_data_json['number']
                        socket_hashMap[receive_number] = self.request
                    else:
                        receive_data_json_value = json.dumps(receive_data_json['value'])
                        methanal_value += receive_data_json_value + ';'
                        times += receive_data_json['time'] + ','
        except OSError as e:
            conn.close()

    def finish(self):
        pass


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 3368), MyServer)
    server.serve_forever()
