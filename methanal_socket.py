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
import schedule
import threading
# from django.shortcuts import HttpResponse
# from rest_framework.views import APIView
socket_hashMap = {}


def heartbeat_wifi():
    for socket_object in socket_hashMap:
        try:
            local_time = datetime.datetime.now()
            local_time_month = str(local_time.month)
            local_time_day = str(local_time.day)
            local_time_hour = str(local_time.hour + 8)
            local_time_minute = str(local_time.minute)
            local_time_result = local_time_month + '-' + local_time_day + '-' + local_time_hour + ':' + local_time_minute
            socket_hashMap[socket_object].send(('connected,' + local_time_result).encode(),)
        except:
            pass


schedule.every(5).seconds.do(heartbeat_wifi)
# schedule.every().hour.do(heartbeat_wifi)


def start_heartbeat():
    while True:
        schedule.run_pending()
        time.sleep(1)


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
            threading.Thread(target=start_heartbeat).start()
            while flag:
                try:
                    receive_data_encode = conn.recv(256)
                    receive_data_decode = receive_data_encode.decode()
                    if receive_data_decode:
                        time.sleep(0.1)
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
                            # conn.close()
                            # time.sleep(610)
                            # flag = False
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
                except:
                    flag = False
                    conn.close()
        except OSError as e:
            conn.close()

    def finish(self):
        pass


if __name__ == '__main__':
    # start_heartbeat()
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 3368), MyServer)
    server.serve_forever()

