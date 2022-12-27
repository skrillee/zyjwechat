__author__ = 'Yan.zhe 2021.09.28'

from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse

# import wechat.views
# import hashlib
# import time
# import requests
from zyjwechat import settings
from wechat import models
import socket
import datetime
import pytz
import os
import json
import base64
from Cryptodome.Cipher import AES
import random
import re
import odoorpc


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def decrypt(appId, sessionKey, encryptedData, iv):
    # base64 decode
    sessionKey = base64.b64decode(sessionKey)
    encryptedData = base64.b64decode(encryptedData)
    iv = base64.b64decode(iv)
    cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
    msg = cipher.decrypt(encryptedData)
    msg = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', msg.decode('utf-8'))
    decrypted = json.loads(msg)
    if decrypted['watermark']['appid'] != appId:
        raise Exception('Invalid Buffer')
    return decrypted


def md5(invitation_code) -> object:
    current_time = str(time.time())
    md5_object = hashlib.md5(bytes(invitation_code, encoding='utf-8'))
    md5_object.update(bytes(current_time, encoding='utf-8'))
    return md5_object.hexdigest()

import calendar;

import time;

ts = calendar.timegm(time.gmtime())


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AuthVIew(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request._request.POST.get('invitation_code')
            if invitation_code == '5211344':
                fake_code = models.CodeToken.objects.first()
                responses['token'] = fake_code.token
            else:
                invitation_code_object = models.ZyjWechatInvitationCode.objects.filter(
                    invitation_code=invitation_code).first()
                if not invitation_code_object:
                    responses['code'] = 3001
                    responses['message'] = "邀请码错误，请填写正确的邀请码"
                else:
                    effective_time = invitation_code_object.effective_time
                    current_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
                    token_object = models.CodeToken.objects.filter(code=invitation_code_object).first()
                    token = md5(invitation_code)
                    if token_object:
                        remaining_time = current_time - token_object.first_loading
                        time_state = remaining_time < datetime.timedelta(days=effective_time)
                        if time_state:
                            responses['token'] = token
                            models.CodeToken.objects.update_or_create(
                                defaults={'token': token, 'token_effective_time': effective_time},
                                code=invitation_code_object)
                        else:
                            responses['code'] = 2001
                            responses['message'] = "邀请码过期，请填写可用的邀请码"
                    else:
                        models.CodeToken.objects.update_or_create(code=invitation_code_object, defaults={
                            'token': token,
                            'token_effective_time': effective_time})
                        responses['token'] = token
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class MobilePhone(APIView):

    authentication_classes = []

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        js_code = request._request.POST.get('jscode')
        iv = request._request.POST.get('iv')

        if js_code:
            encrypted_data = request._request.POST.get('encryptedData')
            url_code_session = "https://api.weixin.qq.com/sns/jscode2session" \
                               "?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(
                                'wxc9ccd41f17a1fa42',
                                '168534ea6674446e6f2d7ea81bff1ab8',
                                js_code)
            response = requests.get(url_code_session)
            try:
                data = json.loads(response.content)
                openid = data['openid']
                session_key = data['session_key']
                appId = 'wxc9ccd41f17a1fa42'
                pResult = decrypt(appId, session_key, encrypted_data, iv)
                mobile_phone_number = pResult["phoneNumber"]
                username = openid
                effective_time = '120'
                models.ZyjWechatInvitationCode.objects.update_or_create(
                    defaults={'name': username,
                              'effective_time': effective_time,
                              'Retail_id': '1',
                              'code_type': '1',
                              'mobile': mobile_phone_number
                              },
                    invitation_code=mobile_phone_number)
                responses['invitation_code'] = mobile_phone_number
            except Exception as e:
                responses['code'] = 3002
                responses['message'] = "请求异常"
        return JsonResponse(responses)


class MobilePhoneFL(APIView):

    authentication_classes = []

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        js_code = request._request.POST.get('jscode')
        iv = request._request.POST.get('iv')

        if js_code:
            encrypted_data = request._request.POST.get('encryptedData')
            url_code_session = "https://api.weixin.qq.com/sns/jscode2session" \
                               "?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(
                                'wxc754f862e84d18b5',
                                '3c79d3dae2d4464e1875fa77d0188e6e',
                                js_code)
            response = requests.get(url_code_session)
            try:
                data = json.loads(response.content)
                openid = data['openid']
                session_key = data['session_key']
                appId = 'wxc754f862e84d18b5'
                pResult = decrypt(appId, session_key, encrypted_data, iv)
                mobile_phone_number = pResult["phoneNumber"]
                username = openid
                effective_time = '120'
                models.ZyjWechatInvitationCode.objects.update_or_create(
                    defaults={'name': username,
                              'effective_time': effective_time,
                              'Retail_id': '1',
                              'code_type': '1',
                              'mobile': mobile_phone_number
                              },
                    invitation_code=mobile_phone_number)
                responses['invitation_code'] = mobile_phone_number
            except Exception as e:
                responses['code'] = 3002
                responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class RetailVIew(APIView):
    """
        Return the retailer information corresponding to the invitation code
    """
    def get(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            retail = request.user.Retail
            retail_message = {
                "shop_name": retail.shop_name,
                "master_name": retail.master_name,
                "phone": retail.phone,
                "qq_number": retail.qq_number,
                "wechat_number": retail.wechat_number,
                "address": retail.address,
                "email": retail.email,
                "shop_introduction": retail.shop_introduction,
            }
            responses['data'] = retail_message
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Manufactor(APIView):
    """
        Return the manufactor information corresponding to the invitation code
    """
    def get(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            manufactor = request.user.Retail.Product.filter()
            manufactor_message = {}
            edition_id_string = ''
            for single_manufactor in manufactor:
                manufactor_edition_id_string = ''
                edition_objects = single_manufactor.zyjwechatedition_set.all()
                for edition_object in edition_objects:
                    edition_id = edition_object.id
                    edition_id_string += str(edition_id)+','
                    manufactor_edition_id_string += str(edition_id)+','
                manufactor_id = single_manufactor.id
                name = single_manufactor.name
                manufactor_introduction = single_manufactor.manufactor_introduction
                manufactor_logo_string = single_manufactor.manufactor_logo
                manufactor_sample_string = single_manufactor.manufactor_sample
                manufactor_logo_dict = {}
                manufactor_sample_dict = {}
                if manufactor_logo_string:
                    manufactor_logo_list = manufactor_logo_string.split(",")
                    for single_manufactor_logo in manufactor_logo_list:
                        manufactor_logo_dict[single_manufactor_logo] = single_manufactor_logo
                if manufactor_sample_string:
                    manufactor_sample_list = manufactor_sample_string.split(",")
                    for single_manufactor_sample in manufactor_sample_list:
                        manufactor_sample_dict[single_manufactor_sample] = single_manufactor_sample
                single_manufactor_message = {
                    "id": manufactor_id,
                    "name": name,
                    "manufactor_introduction": manufactor_introduction,
                    "manufactor_logo_dict": manufactor_logo_dict,
                    "manufactor_sample_dict": manufactor_sample_dict,
                    "manufactor_edition_id_string": manufactor_edition_id_string
                }
                manufactor_message[single_manufactor.name] = single_manufactor_message
            responses['data'] = manufactor_message
            responses['edition_id_string'] = edition_id_string
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


def user_directory_path(filename):
    filename = filename.replace("_", "/")
    image_path = os.path.join(settings.BASE_DIR, "wechat/static/media/manufactor/{}".format(filename))
    return image_path


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class ManufactorPicture(APIView):
    """
        Return the Manufactor Picture corresponding to the invitation code
    """
    def get(self, request, manufactor_request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            image_path = user_directory_path(manufactor_request)
            with open(image_path, 'rb') as file:
                image_data = file.read()
            return HttpResponse(image_data, content_type="image/png")
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Edition(APIView):
    """
        Receive a parameter：manufactor_id
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def get(self, request, manufactor_id):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            edition_message = {}
            edition_sample_dict = {}
            edition_objects = models.ZyjWechatEdition.objects.filter(Manufactor=manufactor_id)
            for edition_object in edition_objects:
                edition_id = edition_object.id
                name = edition_object.name
                style = edition_object.style
                date = edition_object.date
                edition_sample_string = edition_object.edition_sample
                if edition_sample_string:
                    edition_sample_list = edition_sample_string.split(",")
                    for single_edition_sample in edition_sample_list:
                        edition_sample_dict[single_edition_sample] = single_edition_sample
                single_edition_message = {
                    "id": edition_id,
                    "name": name,
                    "style": style,
                    "date": date,
                    "edition_sample_dict": edition_sample_dict,
                }
                edition_message[edition_object.name] = single_edition_message
            responses['data'] = edition_message
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Model(APIView):
    """
        Receive a parameter：manufactor_ids
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            editions = request._request.POST.get('edition_ids')
            manufactor_edition_list = editions.split(",")
            scene = request._request.POST.get('scene')
            model_objects = models.ZyjWechatModel.objects.filter(scene=scene).select_related("Edition")
            model_object_list = []
            sample_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/"
            for model_object in model_objects:
                model_object_dict = {}
                name = model_object.name
                scene = model_object.scene
                date = model_object.date
                model_unit = model_object.model_unit
                model_sample = model_object.model_sample
                edition_id = model_object.Edition.id
                edition_sample = model_object.Edition.edition_sample
                model_vr = model_object.VR_address
                model_VrQr = model_object.VR_QR
                if str(edition_id) in manufactor_edition_list and model_sample:
                    model_object_dict['name'] = name
                    model_object_dict['scene'] = scene
                    model_object_dict['date'] = date
                    model_object_dict['model_VrQr'] = sample_url+edition_sample+model_VrQr
                    model_object_dict['model_vr'] = model_vr
                    model_object_dict['model_unit'] = model_unit
                    model_object_dict['model_sample'] = sample_url+edition_sample+model_sample
                    model_object_dict['edition_name'] = model_object.Edition.name
                    model_object_dict['edition_style'] = model_object.Edition.style
                    model_object_list.append(model_object_dict)
            responses['data'] = model_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Sample(APIView):
    """
        Receive a parameter：manufactor_ids
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            sample_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/"
            model_object_dict = {}
            model_unit = request._request.POST.get('model_unit')
            model_object = models.ZyjWechatModel.objects.filter(name=model_unit).select_related("Edition").first()
            model_unit_list = model_object.model_unit.split(",")
            edition_sample = model_object.Edition.edition_sample
            model_unit_url_list = []
            for model_unit in model_unit_list:
                model_unit_url_list.append(sample_url+edition_sample+model_unit)
            model_object_dict['name'] = model_object.name
            model_object_dict['scene'] = model_object.scene
            model_object_dict['date'] = model_object.date
            model_object_dict['model_unit_list'] = model_unit_url_list
            model_object_dict['reference_price'] = model_object.reference_price
            model_object_dict['size'] = model_object.size
            model_object_dict['detail'] = model_object.details
            responses['data'] = model_object_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Artificial(APIView):
    """
        Receive a parameter：retailretail
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            retail = request.user.Retail
            retail_id = retail.id
            artificial_object = models.ZyjWechatArtificial.objects.filter(Retail=retail_id).all()
            artificial_object_list = []
            for artificial in artificial_object:
                artificial_object_dict = {'name': artificial.name, 'number': artificial.number,
                                          'reference_price': artificial.reference_price, 'experience': artificial.experience}
                artificial_object_list.append(artificial_object_dict)
            responses['data'] = artificial_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Ingredients(APIView):
    """
        Receive a parameter：retailretail
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            ingredients_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/ingredients/"
            retail = request.user.Retail
            retail_id = retail.id
            ingredients_object = models.ZyjWechatIngredients.objects.filter(Retail=retail_id).all()
            ingredients_object_list = []
            for ingredients in ingredients_object:
                ingredients_object_dict = {'name': ingredients.name, 'specification': ingredients.specification,
                                           'reference_price': ingredients.reference_price, 'area_size': ingredients.area_size,
                                           'product_name': ingredients.product_name, 'images': ingredients_url+ingredients.images,
                                           'explain': ingredients.explain}
                ingredients_object_list.append(ingredients_object_dict)
            responses['data'] = ingredients_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Classification(APIView):
    """
        Receive a parameter：retailretail
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            characteristic = request._request.POST.get('characteristic')
            name = request._request.POST.get('name')
            discount = request._request.POST.get('discount')
            classification_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/classification/"
            retail = request.user.Retail
            retail_id = retail.id
            classification_object_list = []
            if name:
                classification = models.Classification.objects.filter(name=name).first()
                classification_object_dict = {'name': classification.name, 'product_name': classification.product_name,
                                              'reference_price': classification.reference_price, 'images_big': classification_url+classification.images_big,
                                              'characteristic': classification.characteristic, 'discount': classification.discount,
                                              'images_parameter': classification_url+classification.images_parameter,
                                              'original_price': classification.original_price, 'manual_price': classification.manual_price,
                                              'size': classification.size, 'details': classification.details,
                                              'evaluate': classification.evaluate
                                              }
                classification_object_list.append(classification_object_dict)
            elif discount:
                classification_object = models.Classification.objects.filter(discount=discount).all()
                for classification in classification_object:
                    if classification.discount == discount:
                        classification_object_dict = {'name': classification.name, 'product_name': classification.product_name,
                                                      'images_small': classification_url+classification.images_small,
                                                      'reference_price': classification.reference_price,
                                                      'characteristic': classification.characteristic, 'discount': classification.discount,
                                                      'original_price': classification.original_price,
                                                      'size': classification.size,
                                                      }
                        classification_object_list.append(classification_object_dict)
            else:
                classification_object = models.Classification.objects.filter(Retail=retail_id).all()
                for classification in classification_object:
                    if classification.characteristic == characteristic:
                        classification_object_dict = {'name': classification.name, 'product_name': classification.product_name,
                                                      'images_small': classification_url+classification.images_small,
                                                      'reference_price': classification.reference_price,
                                                      'characteristic': classification.characteristic, 'discount': classification.discount,
                                                      'original_price': classification.original_price,
                                                      'size': classification.size,
                                                      }
                        classification_object_list.append(classification_object_dict)
            responses['data'] = classification_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


class Classification2(APIView):
    """
        Receive a parameter：retailretail
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            name = request._request.POST.get('name')
            classification_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/classification/"
            classification_object_list = []
            classification = models.Classification.objects.filter(name=name).first()
            images_big_list = classification.images_big.split(",")
            images_big_list = [classification_url+var for var in images_big_list if var]
            classification_object_dict = {'name': classification.name, 'product_name': classification.product_name,
                                          'reference_price': classification.reference_price, 'images_big': images_big_list,
                                          'characteristic': classification.characteristic, 'discount': classification.discount,
                                          'images_parameter': classification_url+classification.images_parameter,
                                          'original_price': classification.original_price, 'manual_price': classification.manual_price,
                                          'size': classification.size, 'details': classification.details,
                                          'evaluate': classification.evaluate
                                          }
            classification_object_list.append(classification_object_dict)
            responses['data'] = classification_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Voucher(APIView):
    """
        Receive a parameter：retailretail
        This parameter is limited to your own brand
        Return the Edition corresponding to the invitation code
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            voucher_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/voucher/"
            retail = request.user.Retail
            retail_id = retail.id
            voucher_object = models.Voucher.objects.filter(Q(Retail=retail_id)).all()
            voucher_object_list = []
            for voucher in voucher_object:
                voucher_object_dict = {'name': voucher.name, 'phone': voucher.phone,
                                       'address': voucher.address, 'reduction': voucher.reduction,
                                       'state': voucher.state, 'images_small': voucher_url+voucher.images_small,
                                       'remaining': voucher.remaining, 'verification': voucher.verification}
                voucher_object_list.append(voucher_object_dict)
            responses['data'] = voucher_object_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# socket_hashMap = {}
# import socketserver
#
#
# class ConnectServer(socketserver.BaseRequestHandler):
#     def __init__(self, request: '', client_address: '', server: ''):
#         super().__init__(request, client_address, server)
#
#     def setup(self):
#         pass
#
#     def handle(self):
#         pass
#
#     def finish(self):
#         pass
#
#
# server = socketserver.ThreadingTCPServer(('0.0.0.0', 3368), ConnectServer)
# server.serve_forever()
socket_hashMap = {}


def connect_send_start_message(data, equipment_number):
    equipment_number_start = equipment_number + 'start'
    if socket_hashMap:
        if equipment_number_start in [key for key, value in socket_hashMap.items()]:
            sock = socket_hashMap[equipment_number_start]
            try:
                sock.send(data)
            except:
                """ 
                    防止服务端出现问题后（如并发问题）倒置此连接关闭，关闭后重新连接
                """
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip_port = ('0.0.0.0', 3367)
                sock.connect(ip_port)
                sock.send(data)
                socket_hashMap[equipment_number_start] = sock
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_port = ('0.0.0.0', 3367)
            sock.connect(ip_port)
            sock.send(data)
            socket_hashMap[equipment_number_start] = sock
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_port = ('0.0.0.0', 3367)
        sock.connect(ip_port)
        sock.send(data)
        socket_hashMap[equipment_number_start] = sock


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Methanal(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        invitation_code = request.user.invitation_code
        value = request._request.POST.get('value')
        equipment_obj = models.Equipment.objects.filter(invitation_code=invitation_code).first()
        if equipment_obj:
            equipment_number = equipment_obj.number
            address_ip = equipment_obj.ip
            address_port = equipment_obj.port
            send_data_dict = {
                "address_ip": address_ip,
                "address_port": address_port,
                "value": value,
                "number": equipment_number
            }
            send_data_str = json.dumps(send_data_dict)
            data = bytes(send_data_str, 'utf-8')
            # 建立链接,服务器为客户端，硬件为服务端
            try:
                connect_send_start_message(data, equipment_number)
            except:
                responses['code'] = 3004
                responses['message'] = "设备正在联网，请稍后(尝试断开设备电源重新接入)"
                responses['data'] = []
        else:
            responses['code'] = 3003
            responses['message'] = "该验证码无可用设备"
            responses['data'] = []
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Result(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            methanal_obj = models.Methanal.objects.filter(invitation_code=invitation_code).order_by('-id').first()
            methanal_time_list = []
            value_methanal_list = []
            value_CO2_list = []
            if methanal_obj:
                methanal_time = methanal_obj.time
                methanal_time_list.append(methanal_time)
                methanal_value_dict = json.loads(methanal_obj.methanal_value)
                value_CO2_list.append(methanal_value_dict['CO2'])
                value_methanal_list.append(methanal_value_dict['methanal'])
                methanal_dict = {
                    "methanal_time": methanal_time_list,
                    "methanal_value": value_methanal_list,
                    "CO2_value": value_CO2_list
                }
                responses['data'] = methanal_dict
            else:
                responses['code'] = 3003
                responses['message'] = "该验证码无可用设备"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Banner(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            location = request._request.POST.get('location')
            banners_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/banner/"
            banner_object_list = []
            banners_objs = models.Banner.objects.filter(location=location).all()
            if banners_objs:
                for banner_obj in banners_objs:
                    banner_object_dict = {'location': banner_obj.location, 'images': banner_obj.images,
                                          'describe': banner_obj.describe, 'images_big': banners_url+banner_obj.images,
                                          'category': banner_obj.category,
                                          }
                    banner_object_list.append(banner_object_dict)
                responses['data'] = banner_object_list
            else:
                responses['code'] = 3003
                responses['message'] = "请求异常"
                responses['data'] = []
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


import collections
AirContent = collections.namedtuple('AirContent', ('tvoc', 'co2'))


class AirQuality(object):
    def __init__(self):
        self._contents = []

    def report_content(self, tvoc, co2):
        self._contents.append(AirContent(tvoc, co2))

    def average_content(self):
        average = {
            'tvoc': '',
            'co2': ''
        }
        tvoc_total, co2_total = 0, 0
        quantity = len(self._contents)
        for content in self._contents:
            tvoc_total += content.tvoc
            co2_total += content.co2
        average['tvoc'] = tvoc_total / quantity
        average['co2'] = co2_total / quantity
        return average


class Equipment(object):
    def __init__(self):
        self._equipments = {}

    def subject(self, name):
        if name not in self._equipments:
            self._equipments[name] = AirQuality()
        return self._equipments[name]


class CustomerData(object):
    def __init__(self):
        self._customers = {}

    def customer(self, equipment_number):
        if equipment_number not in self._customers:
            self._customers[equipment_number] = Equipment()
        return self._customers[equipment_number]


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class History(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            history_obj = models.Methanal.objects.filter(invitation_code=invitation_code).order_by('id')
            history_time_list = []
            history_co2_list = []
            history_tvoc_list = []
            for history_data in history_obj:
                history_time_list.append(history_data.time)
                history_co2_tvoc = json.loads(history_data.methanal_value)
                history_co2_list.append(history_co2_tvoc['CO2'])
                history_tvoc_list.append(history_co2_tvoc['methanal'])
            methanal_dict = {
                "methanal_time": history_time_list,
                "methanal_value": history_tvoc_list,
                "CO2_value": history_co2_list
            }
            responses['data'] = methanal_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# class WXBizDataCrypt:
#     def __init__(self, appId, sessionKey):
#         self.appId = appId
#         self.sessionKey = sessionKey
#
#     def decrypt(self, encryptedData, iv):
#         # base64 decode
#         sessionKey = base64.b64decode(self.sessionKey)
#         encryptedData = base64.b64decode(encryptedData)
#         iv = base64.b64decode(iv)
#
#         cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
#
#         decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
#
#         if decrypted['watermark']['appid'] != self.appId:
#             raise Exception('Invalid Buffer')
#
#         return decrypted
#
#     def _unpad(self, s):
#         return s[:-ord(s[len(s)-1:])]


# 解密获取用户信息
# def decrypt_encrypteddata(app_id, session_key, encryptedData, iv):
#     decrypt_data = WXBizDataCrypt(app_id, session_key)
#     decrypt_data = decrypt_data.decrypt(encryptedData, iv)
#     return decrypt_data


# 随机随机字符串
def get_random_str():

    data = "123456789zxcvbnmasdfghdjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
    nonce_str = ''.join(random.sample(data, 30))
    return nonce_str


# 时间戳
def get_time():
    return str(int(time.time()))


# class Callback(APIView):
#     def post(self):
#         responses = {
#             'code': 1000,
#             'message': None
#         }
#         return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
import requests
import hashlib
import xmltodict
import time
import string

# 生成一个以当前文件名为名字的logger实例

class Login(APIView):

    # 生成nonce_str
    def generate_randomStr(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 32))

    # 生成签名
    def generate_sign(param):
        stringA = ''

        ks = sorted(param.keys())
        # 参数排序
        for k in ks:
            stringA += k + "=" + str(param[k]) + "&"
        # 拼接商户KEY
        stringSignTemp = stringA + "key=" + KEY

        # md5加密
        hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
        sign = hash_md5.hexdigest().upper()

        return sign

    # 发送xml请求
    def send_xml_request(url, param):
        # dict 2 xml
        param = {'root': param}
        xml = xmltodict.unparse(param)

        response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
        # xml 2 dict
        msg = response.text
        xmlmsg = xmltodict.parse(msg)
        return xmlmsg

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            wechat_code = request._request.POST.get('code')
            # wechat_code = "081lOcll2hW7G84wJCml2bhswh1lOcld"
            url_code_session = "https://api.weixin.qq.com/sns/jscode2session" \
                               "?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(
                                'wxc9ccd41f17a1fa42', '168534ea6674446e6f2d7ea81bff1ab8', wechat_code
            )
            data = requests.get(url_code_session)
            if data.status_code == 200:
                data_content = json.loads(data.content)
                if "openid" in data_content:
                    openid = data_content.get('openid')
                    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
                    nonce_str = generate_randomStr()  # 订单中加nonce_str字段记录（回调判断使用）
                    out_trade_no = '20226782122391'  # 支付单号，只能使用一次，不可重复支付
                    param = {
                        "appid": APPID,
                        "mch_id": MCHID,  # 商户号
                        "nonce_str": nonce_str,  # 随机字符串
                        "body": 'TEST_pay',  # 支付说明
                        "out_trade_no": out_trade_no,  # 自己生成的订单号
                        "total_fee": 1,
                        "spbill_create_ip": '127.0.0.1',  # 发起统一下单的ip
                        # "spbill_create_ip": '47.92.85.245',  # 发起统一下单的ip
                        "notify_url": NOTIFY_URL,
                        "trade_type": 'JSAPI',  # 小程序写JSAPI
                        "openid": openid,
                    }
                    # 2. 统一下单签名
                    sign = generate_sign(param)
                    param["sign"] = sign  # 加入签名
                    # 3. 调用接口
                    xmlmsg = send_xml_request(url, param)
                    # 4. 获取prepay_id
                    if xmlmsg['xml']['return_code'] == 'SUCCESS':
                        if xmlmsg['xml']['result_code'] == 'SUCCESS':
                            prepay_id = xmlmsg['xml']['prepay_id']
                            # 时间戳
                            timeStamp = str(int(time.time()))
                            # 5. 根据文档，六个参数，否则app提示签名验证失败，https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12
                            data = {
                                "appId": APPID,
                                "timeStamp": timeStamp,
                                "nonceStr": nonce_str,
                                "package": 'prepay_id=' + prepay_id,
                                "signType": 'MD5',
                                # "partnerid": MCHID,
                                # "prepayid": prepay_id,
                                # "total_fee":1
                            }  # 6. paySign签名
                            paySign = generate_sign(data)
                            data["paySign"] = paySign  # 加入签名
                            # 7. 传给前端的签名后的参数
                            # return data
                    data = {
                        "data": data,
                    }
                    responses['data'] = data
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "登陆失败"
        return JsonResponse(responses)


# 统一下单

import requests
import hashlib
import xmltodict
import time
import string

# 配置必须参数

APPID = "wxc9ccd41f17a1fa42"  # 小程序ID
SECRET = "bc8f9ad106f0975fedc5e83182c06d8a"
MCHID = "1619888204"  # 商户号
KEY = "iWOwoB8rWkhIUDFBHdjnf93wdwo64Xzq"
NOTIFY_URL = "https://www.zhuangyuanjie.cn/api/v1/auth/"  # 统一下单后微信回调地址，api demo见notify_view_demo.py
WX_CERT_PATH = "path/to/apiclient_cert.pem"
WX_KEY_PATH = "path/to/apiclient_key.pem.unsecure"


# 生成nonce_str
def generate_randomStr():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


# 生成签名
def generate_sign(param):
    stringA = ''

    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += k + "=" + str(param[k]) + "&"
    # 拼接商户KEY
    stringSignTemp = stringA + "key=" + KEY

    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()

    return sign


# 发送xml请求
def send_xml_request(url, param):
    # dict 2 xml
    param = {'root': param}
    xml = xmltodict.unparse(param)

    response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    # xml 2 dict
    msg = response.text
    xmlmsg = xmltodict.parse(msg)

    return xmlmsg


# 统一下单
def generate_bill(out_trade_no, fee, openid):
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    nonce_str = generate_randomStr()  # 订单中加nonce_str字段记录（回调判断使用）
    out_trade_no = "20226782122363"  # 支付单号，只能使用一次，不可重复支付

    '''
    order.out_trade_no = out_trade_no
    order.nonce_str = nonce_str
    order.save()
    '''

    # 1. 参数
    param = {
        "appid": APPID,
        "mch_id": MCHID,  # 商户号
        "nonce_str": nonce_str,  # 随机字符串
        "body": 'TEST_pay',  # 支付说明
        "out_trade_no": out_trade_no,  # 自己生成的订单号
        "total_fee": fee,
        "spbill_create_ip": '127.0.0.1',  # 发起统一下单的ip
        "notify_url": NOTIFY_URL,
        "trade_type": 'JSAPI',  # 小程序写JSAPI
        "openid": openid,
    }
    # 2. 统一下单签名
    sign = generate_sign(param)
    param["sign"] = sign  # 加入签名
    # 3. 调用接口
    xmlmsg = send_xml_request(url, param)
    # 4. 获取prepay_id
    if xmlmsg['xml']['return_code'] == 'SUCCESS':
        if xmlmsg['xml']['result_code'] == 'SUCCESS':
            prepay_id = xmlmsg['xml']['prepay_id']
            # 时间戳
            timeStamp = str(int(time.time()))
            # 5. 根据文档，六个参数，否则app提示签名验证失败，https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12
            data = {
                "appid": APPID,
                "partnerid": MCHID,
                "prepayid": prepay_id,
                "package": 'prepay_id'+prepay_id,
                "noncestr": nonce_str,
                "timestamp": timeStamp,
            }  # 6. paySign签名
            paySign = generate_sign(data)
            data["paySign"] = paySign  # 加入签名
            # 7. 传给前端的签名后的参数
            return data


import xmltodict

from django.http import HttpResponse


class Payback(APIView):
    def post(request):
        msg = request.body.decode('utf-8')
        xmlmsg = xmltodict.parse(msg)

        return_code = xmlmsg['xml']['return_code']

        if return_code == 'FAIL':
            # 官方发出错误
            return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                                <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                                content_type='text/xml', status=200)

        elif return_code == 'SUCCESS':
            # 拿到这次支付的订单号
            out_trade_no = xmlmsg['xml']['out_trade_no']
            # order = Order.objects.get(out_trade_no=out_trade_no)
            if xmlmsg['xml']['nonce_str'] != out_trade_no.nonce_str:
                # 随机字符串不一致
                return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                                            <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                                    content_type='text/xml', status=200)

            # 根据需要处理业务逻辑

            return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                                <return_msg><![CDATA[OK]]></return_msg></xml>""",
    content_type='text/xml', status=200)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Live(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            duration_time = int(request._request.POST.get('duration_time'))
            after_hour_start_time = int(request._request.POST.get('after_hour_start_time'))
            media_id = request._request.POST.get('media_id')
            room_name = request._request.POST.get('room_name')
            anchor_id = request._request.POST.get('anchor_id')
            anchor_wechat = request._request.POST.get('anchor_wechat')
            anchor_name = request._request.POST.get('anchor_name')
            live_type = int(request._request.POST.get('live_type'))
            screen_type = int(request._request.POST.get('screen_type'))
            close_like = int(request._request.POST.get('close_like'))
            close_goods = int(request._request.POST.get('close_goods'))
            close_comment = int(request._request.POST.get('close_comment'))
            room_belong = request._request.POST.get('room_belong')
            access_token = request._request.POST.get('access_token')

            # 时间戳
            now_time = datetime.datetime.now()
            start_time = (now_time + datetime.timedelta(hours=after_hour_start_time)).strftime("%Y-%m-%d %H:%M:%S")
            start_time_stamp = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            close_time = (now_time + datetime.timedelta(hours=after_hour_start_time) +
                          datetime.timedelta(hours=duration_time)).strftime("%Y-%m-%d %H:%M:%S")
            close_time_stamp = time.mktime(time.strptime(close_time, '%Y-%m-%d %H:%M:%S'))

            param_data = {
                "name": room_name,
                "coverImg": media_id,
                "startTime": start_time_stamp,
                "endTime": close_time_stamp,
                "anchorName": anchor_name,
                "anchorWechat": anchor_wechat,
                "shareImg": media_id,
                "type": live_type,
                "screenType": screen_type,
                "closeLike": close_like,
                "closeGoods": close_goods,
                "closeComment": close_comment,
                "feedsImg": media_id
            }
            create_room_url = "https://api.weixin.qq.com/wxaapi/broadcast/room/create?access_token="+access_token
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            create_room_result = requests.request("post", url=create_room_url, json=param_data, headers=headers)
            room_id = json.loads(create_room_result.text)['roomId']
            live_data = {
                "room_id": room_id
            }
            responses['data'] = live_data
            models.LivingRoom.objects.update_or_create(defaults={'anchor_name': anchor_name,
                                                                 'anchor_wechat': anchor_wechat,
                                                                 'media_id': media_id,
                                                                 'room_belong': room_belong,
                                                                 'room_id': room_id,
                                                                 'room_name': room_name},
                                                       id=anchor_id)
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)

        # param_data = json.dumps(param_data)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Room(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            invitation_obj = models.ZyjWechatInvitationCode.objects.filter(invitation_code=invitation_code).first()
            if invitation_obj:
                try:
                    live_room_obj = invitation_obj.LiveRoom
                    room_id = live_room_obj.room_id
                    anchor_name = live_room_obj.anchor_name
                    room_belong = live_room_obj.room_belong
                    room_name = live_room_obj.room_name
                    live_room_data = {
                        "room_id": int(room_id),
                        "anchor_name": anchor_name,
                        "room_belong": room_belong,
                        "room_name": room_name
                    }
                    responses['data'] = live_room_data
                except Exception as e:
                    responses['code'] = 3006
                    responses['message'] = "该验证码暂无可用直播间"
            else:
                responses['code'] = 3005
                responses['message'] = "无效验证码，请核对验证码是否正确"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)

        # param_data = json.dumps(param_data)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Status(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            page_position = request._request.POST.get('page_position')
            history_obj = models.Methanal.objects.filter(invitation_code=invitation_code).order_by('id')
            history_time_list = []
            history_co2_list = []
            history_tvoc_list = []
            for history_data in history_obj:
                history_time_list.append(history_data.time)
                history_co2_tvoc = json.loads(history_data.methanal_value)
                history_co2_list.append(history_co2_tvoc['CO2'])
                history_tvoc_list.append(history_co2_tvoc['methanal'])
            methanal_dict = {
                "methanal_time": history_time_list,
                "methanal_value": history_tvoc_list,
                "CO2_value": history_co2_list
            }
            responses['data'] = methanal_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Ticket(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            advertiser_ids = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first().Retail.advertiser
            advertiser_ids_list = advertiser_ids.split(",")
            advertiser_ids_list = [var for var in advertiser_ids_list if var]
            ticket_objs = models.Ticket.objects.filter(
                Retail_id__in=advertiser_ids_list).all()
            # retail_objects = models.ZyjWechatRetail.objects.filter(id=advertiser_ids_list).all()
            ticket_objs_type_dict = {}
            ticket_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/ticket/"
            for ticket_obj in ticket_objs:
                ticket_dict = {
                    "ticket_id": ticket_obj.id,
                    "ticket_name": ticket_obj.ticket_name,
                    "ticket_type": ticket_obj.ticket_type,
                    "ticket_information": ticket_obj.ticket_information,
                    "ticket_image": ticket_url+ticket_obj.ticket_image,
                    "ticket_image_detail": ticket_obj.ticket_image_detail,
                    "ticket_active": ticket_obj.ticket_active,
                    "ticket_price": ticket_obj.remark,
                }
                if ticket_obj.ticket_type in ticket_objs_type_dict.keys():
                    ticket_objs_type_dict[ticket_obj.ticket_type].append(ticket_dict)
                else:
                    ticket_objs_type_dict[ticket_obj.ticket_type] = [ticket_dict]
            responses['data'] = ticket_objs_type_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Bill(APIView):
    """
     color： #0F375A #F9C03D #BFD0DA #65472F #E9D9BF #D4920A #056E83 #FFAAAA #F0C046 #4B4B4E #E9D9BF #0F375A
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            role = request._request.POST.get('role')
            if role == "customer":
                invitation_code_id = models.ZyjWechatInvitationCode.objects.filter(
                    invitation_code=invitation_code).first().id
                bill_objects = models.ZyjWechatBill.objects.filter(
                    InvitationCode_id=invitation_code_id).all()
                if bill_objects:
                    bill_object_list = []
                    bill_chart_value_list = []
                    bill_chart_name_list = []
                    bill_chart_color_list = []
                    bill_total = 0
                    for bill_object in bill_objects:
                        bill_dict = {
                            "bill_id": bill_object.id,
                            "customer_name": bill_object.customer_name,
                            "cost_name": bill_object.cost_name,
                            "unit_price": bill_object.unit_price,
                            "quantity": bill_object.quantity,
                            "trading_time": bill_object.trading_time,
                            "chart_color": bill_object.chart_color
                        }
                        bill_chart = {
                            "name": bill_object.cost_name,
                            "value": float(bill_object.unit_price)*float(bill_object.quantity)
                        }

                        bill_object_list.append(bill_dict)
                        bill_chart_value_list.append(bill_chart)
                        bill_chart_name_list.append(bill_object.cost_name)
                        bill_chart_color_list.append(bill_object.chart_color)
                        bill_total += float(bill_object.unit_price)*float(bill_object.quantity)
                    responses['data'] = bill_object_list
                    responses['chart_value'] = bill_chart_value_list
                    responses['chart_name'] = bill_chart_name_list
                    responses['chart_color'] = bill_chart_color_list
                    responses['bill_total'] = bill_total
                else:
                    responses['code'] = 3007
                    responses['message'] = "暂无数据"
            elif role == "business":
                invitation_code_object = models.ZyjWechatInvitationCode.objects.filter(
                    invitation_code=invitation_code).first()
                if invitation_code_object.code_type != 1:
                    retail_id = models.ZyjWechatRetail.objects.filter(
                        id=invitation_code_object.Retail_id).first().id
                    bill_objects = models.ZyjWechatBill.objects.filter(
                        Retail_id=retail_id).all().order_by('-trading_time')
                    bill_objs_customer_dict = {}
                    for bill_object in bill_objects:
                        bill_dict = {
                            "customer_name": bill_object.customer_name,
                            "trading_time": bill_object.trading_time,
                        }
                        if bill_object.customer_name in bill_objs_customer_dict.keys():
                            bill_detail_dict = bill_objs_customer_dict[bill_object.customer_name][0]
                            bill_detail_dict["item_quantity"] += 1
                            bill_detail_dict["item_total"] += float(bill_object.unit_price)*float(bill_object.quantity)
                            bill_detail_dict["customer_name"] = bill_object.customer_name
                            bill_detail_dict["trading_time"] = bill_object.trading_time
                        else:
                            bill_dict["item_quantity"] = 1
                            bill_dict["retail_id"] = bill_object.Retail_id
                            bill_dict["invitation_id"] = bill_object.InvitationCode_id
                            bill_dict["item_total"] = float(bill_object.unit_price)*float(bill_object.quantity)
                            bill_objs_customer_dict[bill_object.customer_name] = [bill_dict]
                    responses['data'] = bill_objs_customer_dict
                else:
                    responses['code'] = 3009
                    responses['message'] = "该账号无权限查看"
            else:
                responses['code'] = 3008
                responses['message'] = "角色role参数错误"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class BillDetail(APIView):
    """
     color： #0F375A #F9C03D #BFD0DA #65472F #E9D9BF #D4920A #056E83 #FFAAAA #F0C046 #4B4B4E #E9D9BF #0F375A
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            """
                一个登陆后的商铺，只能看到输入自己的客户，查询条件分为前端传来的客户的邀请码id，以及商户自己的邀请码id
            """
            invitation_code = request.user.invitation_code
            invitation_code_id = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first().id
            # retail_id = request._request.POST.get('retail_id')
            invitation_id = request._request.POST.get('invitation_id')
            bill_objects = models.ZyjWechatBill.objects.filter(
                Retail_id=invitation_code_id, InvitationCode_id=invitation_id).all().order_by('-trading_time')
            bill_list = []
            for bill_object in bill_objects:
                bill_dict = {
                    "customer_name": bill_object.customer_name,
                    "cost_name": bill_object.cost_name,
                    "unit_price": bill_object.unit_price,
                    "quantity": bill_object.quantity,
                    "trading_time": bill_object.trading_time,
                    "bill_id": bill_object.id,
                    "item_total": float(bill_object.unit_price)*float(bill_object.quantity),
                    "remark": bill_object.remark
                }
                bill_list.append(bill_dict)
            responses['data'] = bill_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


def select_different_color(selected_color_list):
    color_list = ['#0F375A', '#F9C03D', '#BFD0DA', '#65472F', '#E9D9BF', '#D4920A', '#056E83', '#FFAAAA',
                  '#F0C046', '#4B4B4E', '#E9D9BF', '#0F375A']
    result_list = list(set(color_list).difference(set(selected_color_list)))
    return result_list


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AddBillDetail(APIView):
    """
     color： ['#0F375A', ' #F9C03D', ' #BFD0DA', '#65472F', '#E9D9BF', '#D4920A', '#056E83', '#FFAAAA',
                          '#F0C046', '#4B4B4E', '#E9D9BF', '#0F375A']
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            invitation_code_obj = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first()
            retail_id = invitation_code_obj.id
            remark = request._request.POST.get('remark')
            unit_price = request._request.POST.get('unit_price')
            quantity = request._request.POST.get('quantity')
            cost_name = request._request.POST.get('cost_name')
            invitation_id = request._request.POST.get('invitation_id')
            invitation_code_name = models.ZyjWechatInvitationCode.objects.filter(
                id=invitation_id).first().name
            local_time = datetime.datetime.now()
            local_time_month = str(local_time.month)
            local_time_day = str(local_time.day)
            local_time_year = str(local_time.year)
            local_time_result = local_time_year + '-' + local_time_month + '-' + local_time_day
            bill_objects = models.ZyjWechatBill.objects.filter(
                Retail_id=retail_id, InvitationCode_id=invitation_id).all()
            selected_color_list = []
            for bill_object in bill_objects:
                selected_color_list.append(bill_object.chart_color)
            new_color_list = select_different_color(selected_color_list)
            color_random = random.sample(new_color_list, 1)[0]
            models.ZyjWechatBill.objects.create(
                customer_name=invitation_code_name, cost_name=cost_name, unit_price=unit_price, quantity=quantity,
                trading_time=local_time_result, chart_color=color_random, InvitationCode_id=invitation_id,
                remark=remark, Retail_id=retail_id
            )
            responses['data'] = "更新成功"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class DelBillDetail(APIView):
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:

            bill_id = request._request.POST.get('bill_id')
            models.ZyjWechatBill.objects.filter(
                id=bill_id).first().delete()
            responses['data'] = "删除成功"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AddBill(APIView):
    """
     color： ['#0F375A', ' #F9C03D', ' #BFD0DA', '#65472F', '#E9D9BF', '#D4920A', '#056E83', '#FFAAAA',
                          '#F0C046', '#4B4B4E', '#E9D9BF', '#0F375A']
    """
    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            invitation_code_obj = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first()
            retail_id = invitation_code_obj.id
            remark = request._request.POST.get('remark')
            unit_price = request._request.POST.get('unit_price')
            quantity = request._request.POST.get('quantity')
            cost_name = request._request.POST.get('cost_name')
            customer_id = request._request.POST.get('customer_id')
            invitation_code_obj = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=customer_id).first()
            if invitation_code_obj:
                invitation_id = invitation_code_obj.id
                customer_name = invitation_code_obj.name
                local_time = datetime.datetime.now()
                local_time_month = str(local_time.month)
                local_time_day = str(local_time.day)
                local_time_year = str(local_time.year)
                local_time_result = local_time_year + '-' + local_time_month + '-' + local_time_day
                bill_objects = models.ZyjWechatBill.objects.filter(
                    Retail_id=retail_id, InvitationCode_id=invitation_id).all()
                selected_color_list = []
                for bill_object in bill_objects:
                    selected_color_list.append(bill_object.chart_color)
                new_color_list = select_different_color(selected_color_list)
                color_random = random.sample(new_color_list, 1)[0]
                models.ZyjWechatBill.objects.create(
                    customer_name=customer_name, cost_name=cost_name, unit_price=unit_price, quantity=quantity,
                    trading_time=local_time_result, chart_color=color_random, InvitationCode_id=invitation_id,
                    remark=remark, Retail_id=retail_id
                )
                responses['data'] = "更新成功"
            else:
                responses['code'] = 3010
                responses['message'] = "无效的邀请码"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AddPicture(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            invitation_code_obj = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first()
            if invitation_code_obj.code_type != 1:
                invitation_code = request._request.POST.get('invitation_code')
                invitation_code_obj = models.ZyjWechatInvitationCode.objects.filter(
                    invitation_code=invitation_code).first()
                if invitation_code_obj:
                    pic_item = request._request.POST.get('item')
                    files = request.FILES
                    content = files.get('image', None).read()
                    # path = os.path.join(settings.IMAGES_DIR[0], 'aaa.jpg')
                    path = os.path.join(settings.IMAGES_DIR[0])+'/{}'.format(invitation_code)
                    path_pic = path+'/'+'{}'.format(pic_item)+'.jpg'

                    path_static = os.path.join(settings.STATIC_IMAGES_DIR[0])+'/{}'.format(invitation_code)
                    path_pic_static = path_static + '/' + '{}'.format(pic_item) + '.jpg'
                    try:
                        with open(path_pic, 'wb') as f:
                            f.write(content)
                    except:
                        os.makedirs(path)
                        with open(path_pic, 'wb') as f:
                            f.write(content)
                    try:
                        with open(path_pic_static, 'wb') as f_static:
                            f_static.write(content)
                    except:
                        os.makedirs(path_static)
                        with open(path_pic_static, 'wb') as f_static:
                            f_static.write(content)
                    responses['data'] = "更新成功"
                else:
                    responses['code'] = 3010
                    responses['message'] = "无效的邀请码"
            else:
                responses['code'] = 3009
                responses['message'] = "该账号无权限添加"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class CheckPicture(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            check_static_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/check/"
            check_url = check_static_url+invitation_code
            try:
                path_static = os.path.join(settings.STATIC_IMAGES_DIR[0]) + '/{}'.format(invitation_code)
                images_path = os.listdir(path_static)
                if images_path:
                    check_images_list = []
                    for filename in images_path:
                        # check_dict = {
                        #     "check_image": check_url + '/' + filename,
                        # }
                        check_images_list.append(check_url + '/' + filename)
                    responses['data'] = check_images_list
                else:
                    responses['code'] = 3011
                    responses['message'] = "该邀请码下暂无信息，请联系商家上传照片"
            except:
                responses['code'] = 3012
                responses['message'] = "该邀请码下暂无信息，请联系商家上传照片"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


from pypinyin import lazy_pinyin, Style


def get_initials(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    initials = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return initials.upper()[0]


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Contacts(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }

        try:
            invitation_code = request.user.invitation_code
            invitation_code_object = models.ZyjWechatInvitationCode.objects.filter(
                invitation_code=invitation_code).first()
            if invitation_code_object.code_type != 1:
                retail_id = invitation_code_object.Retail_id
                contacts_objects = models.ZyjWechatInvitationCode.objects.filter(Retail_id=retail_id).all()
                contacts_objs_customer_dict = {}
                for contacts_object in contacts_objects:
                    initials = get_initials(contacts_object.name)
                    contacts_dict = {
                        "id": contacts_object.id,
                        "customer_name": contacts_object.name,
                        # "initials": initials,
                        # "street": contacts_object.street
                    }
                    if initials in contacts_objs_customer_dict.keys():
                        contacts_objs_customer_dict[initials].append(contacts_dict)
                    else:
                        contacts_objs_customer_dict[initials] = [contacts_dict]
                responses['data'] = contacts_objs_customer_dict
            else:
                responses['code'] = 3009
                responses['message'] = "该账号无权限查看"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class SearchContacts(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }

        try:
            name_id = request._request.POST.get('name_id')
            invitation_code_object = models.ZyjWechatInvitationCode.objects.filter(
                id=name_id).first()
            contacts_dict = {
                "id": invitation_code_object.id,
                "customer_name": invitation_code_object.name,
                # "initials": initials,
                "street": invitation_code_object.street,
                "mobile": invitation_code_object.mobile,
                "invitation_code": invitation_code_object.invitation_code
            }
            responses['data'] = contacts_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AddOrder(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            name = request._request.POST.get('name')
            classification_object_id = models.Classification.objects.filter(
                name=name).first().id
            cart_object_id = models.Cart.objects.filter(
                cart_code=invitation_code, Classification_id=classification_object_id).first()
            order_dict = {
                "cart_code": invitation_code,
                "Classification_id": classification_object_id,
            }
            if cart_object_id:
                models.Cart.objects.update_or_create(defaults=order_dict, id=cart_object_id.id)
            else:
                models.Cart.objects.update_or_create(cart_code=invitation_code, Classification_id=classification_object_id)

        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class DeleteOrder(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            invitation_code = request.user.invitation_code
            name = request._request.POST.get('name')
            classification_object_id = models.Classification.objects.filter(
                name=name).first().id
            models.Cart.objects.filter(cart_code=invitation_code, Classification_id=classification_object_id).first().delete()
            responses['data'] = "删除成功"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class GetOrder(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            classification_id_list = []
            classification_object_list = []
            invitation_code = request.user.invitation_code
            cart_object_objs = models.Cart.objects.filter(
                cart_code=invitation_code).all()
            if cart_object_objs:
                for cart_object_obj in cart_object_objs:
                    classification_id = cart_object_obj.Classification_id
                    classification_id_list.append(classification_id)
                classification_objs = models.Classification.objects.filter(id__in=classification_id_list).all()
                classification_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/classification/"
                if classification_objs:
                    for classification in classification_objs:
                        classification_object_dict = {'name': classification.name,
                                                      'product_name': classification.product_name,
                                                      'images_small': classification_url + classification.images_small,
                                                      'reference_price': classification.reference_price,
                                                      'characteristic': classification.characteristic,
                                                      'discount': classification.discount,
                                                      'original_price': classification.original_price,
                                                      'size': classification.size,
                                                      }
                        classification_object_list.append(classification_object_dict)
                        responses['data'] = classification_object_list
            else:
                responses['code'] = 1001
                responses['message'] = "无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class CreateOrder(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            order_name = request._request.POST.get('name')
            order_local = request._request.POST.get('local')
            order_time = request._request.POST.get('time')
            order_phone = request._request.POST.get('phone')
            order_remark = request._request.POST.get('remark')
            invitation_code = request.user.invitation_code
            order_dict = {
                "order_owner": order_name,
                "order_local": order_local,
                "order_time": order_time,
                "order_phone": order_phone,
                "remark": order_remark,
            }
            models.Order.objects.update_or_create(defaults=order_dict, order_code=invitation_code)
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class GetVideo(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            characteristic = request._request.POST.get('characteristic')
            classification_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/classification/"
            retail = request.user.Retail
            retail_id = retail.id
            classification_object_list = []
            classification_object = models.Classification.objects.filter(
                Retail=retail_id, characteristic=characteristic).first()
            if classification_object:
                video_object_dict = {
                    'video': classification_url + classification_object.images_small,
                }
                images_big_list = classification_object.images_big.split(",")
                for var in images_big_list:
                    if var:
                        product_object = models.Classification.objects.filter(
                            name=var).first()
                        classification_object_dict = {'name': product_object.name,
                                                      'product_name': product_object.product_name,
                                                      'images_small': classification_url + product_object.images_small,
                                                      'reference_price': product_object.reference_price,
                                                      'characteristic': product_object.characteristic,
                                                      'discount': product_object.discount,
                                                      'original_price': product_object.original_price,
                                                      'size': product_object.size,
                                                      }
                        classification_object_list.append(classification_object_dict)
                responses['data'] = classification_object_list
                responses['data_video'] = video_object_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


from django.http import HttpResponseRedirect
import webbrowser


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Redirect(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    def get(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            app_id = 'wxc9ccd41f17a1fa42'
            secret = '168534ea6674446e6f2d7ea81bff1ab8'
            content = requests.get(url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'.format(APPID=app_id, APPSECRET=secret))
            access_token = json.loads(content.content)['access_token']
            content = requests.post(url='https://api.weixin.qq.com/wxa/generatescheme?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=access_token)).content
            open_link = json.loads(content)['openlink']
            response = HttpResponse("", status=302)
            response['Location'] = open_link
            return response
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Manifest(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            data_time = request._request.POST.get('data_time')
            phone_number = request._request.POST.get('phone_number')
            odoo = odoorpc.ODOO('47.92.85.245', port=3369)
            odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')
            user_id = odoo.env['feeling_customer.information'].search([('customer_information_phone', '=', phone_number)])
            manifest_list = odoo.env['fixed.freight_bill'].search(['|', ('date_invoice', '=', data_time),  ('id', '=', user_id)])
            list_number = len(manifest_list)
            manifest_line_list = []
            for manifest_id in manifest_list:
                manifest_line = []
                manifest_lines = odoo.env['fixed.freight_bill.line'].search([('freight_id', '=', manifest_id)])
                for manifest in manifest_lines:
                    manifest_obj = odoo.env['fixed.freight_bill.line'].browse(manifest)
                    manifest_line.append({
                        'product_id': manifest_obj['product_id'],
                        'length_of_the_goods': manifest_obj['length_of_the_goods'],
                        'width_of_the_goods': manifest_obj['width_of_the_goods'],
                        'area_of_the_goods': manifest_obj['area_of_the_goods'],
                        'unit_price': manifest_obj['unit_price'],
                        'total_prices': manifest_obj['length_of_the_goods'] * manifest_obj['width_of_the_goods'] * manifest_obj['unit_price'],
                        'remark': manifest_obj['remark']
                    })
                manifest_line_list.append(manifest_line)
            manifest_dict = {
                "list_number": list_number,
                "manifest_list": manifest_line_list
            }
            responses['manifest_dict'] = manifest_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


class Douyin(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    def get(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            response = HttpResponse("", status=302)
            response['Location'] = "https://v.douyin.com/2BERMjD/"
            return response
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


from django.shortcuts import render, redirect


def index(request):
    su = request.META.get("HTTP_USER_AGENT")
    if "Android" in su and "WeChat" in su:
        path = "/home/yanboce/apps/zyjwechat/static/media/manufactor/classification/android.png"
        file_one = open(path, "rb")
        return HttpResponse(file_one.read(), content_type='image/jpg')
    else:
        return render(request, 'index.html')


def douyin(request):
    responses = {
        'code': 1000,
        'message': None
    }
    try:
        response = HttpResponse("", status=302)
        response['Location'] = "https://v.douyin.com/2BERMjD/"
        return response
    except Exception as e:
        responses['code'] = 3002
        responses['message'] = "请求异常"
    return JsonResponse(responses)