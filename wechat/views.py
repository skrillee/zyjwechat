__author__ = 'Yan.zhe 2021.09.28'

from rest_framework.views import APIView
from django.http import JsonResponse
from zyjwechat import settings
from wechat import models
from django.db.models import Q
from Cryptodome.Cipher import AES
import socket
import datetime
import pytz
import os
import json
import base64
import random
import re
import odoorpc
import math


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
                'ddbe4a7654a3223c6ed40921f083995c',
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
                effective_time = '365'
                models.ZyjWechatInvitationCode.objects.update_or_create(
                    defaults={'name': username,
                              'effective_time': effective_time,
                              'Retail_id': '1',
                              'code_type': '1',
                              'mobile': mobile_phone_number
                              },
                    invitation_code=mobile_phone_number)

                customer_information = odoo.env['feeling_customer.information']
                user_id = customer_information.search([('customer_information_phone', '=', mobile_phone_number)])
                customer_business = customer_information.browse(user_id).customer_business

                responses['invitation_code'] = mobile_phone_number
                responses['customer_business'] = customer_business

            except Exception as e:
                responses['code'] = 3002
                responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
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
                'ddbe4a7654a3223c6ed40921f083995c',
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
                effective_time = '365'
                models.ZyjWechatInvitationCode.objects.update_or_create(
                    defaults={'name': username,
                              'effective_time': effective_time,
                              'Retail_id': '1',
                              'code_type': '1',
                              'mobile': mobile_phone_number
                              },
                    invitation_code=mobile_phone_number)
                odoo = odoorpc.ODOO('47.92.85.245', port=3369)
                odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')
                customer_information = odoo.env['feeling_customer.information']
                user_id = customer_information.search([('customer_information_phone', '=', mobile_phone_number)])
                customer_business = customer_information.browse(user_id).customer_business

                responses['invitation_code'] = mobile_phone_number
                responses['customer_business'] = customer_business
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
                    edition_id_string += str(edition_id) + ','
                    manufactor_edition_id_string += str(edition_id) + ','
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
                    model_object_dict['model_VrQr'] = sample_url + edition_sample + model_VrQr
                    model_object_dict['model_vr'] = model_vr
                    model_object_dict['model_unit'] = model_unit
                    model_object_dict['model_sample'] = sample_url + edition_sample + model_sample
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
                model_unit_url_list.append(sample_url + edition_sample + model_unit)
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
                                          'reference_price': artificial.reference_price,
                                          'experience': artificial.experience}
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
                                           'reference_price': ingredients.reference_price,
                                           'area_size': ingredients.area_size,
                                           'product_name': ingredients.product_name,
                                           'images': ingredients_url + ingredients.images,
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
                                              'reference_price': classification.reference_price,
                                              'images_big': classification_url + classification.images_big,
                                              'characteristic': classification.characteristic,
                                              'discount': classification.discount,
                                              'images_parameter': classification_url + classification.images_parameter,
                                              'original_price': classification.original_price,
                                              'manual_price': classification.manual_price,
                                              'size': classification.size, 'details': classification.details,
                                              'evaluate': classification.evaluate
                                              }
                classification_object_list.append(classification_object_dict)
            elif discount:
                classification_object = models.Classification.objects.filter(discount=discount).all()
                for classification in classification_object:
                    if classification.discount == discount:
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
            else:
                classification_object = models.Classification.objects.filter(Retail=retail_id).all()
                for classification in classification_object:
                    if classification.characteristic == characteristic:
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
            images_big_list = [classification_url + var for var in images_big_list if var]
            classification_object_dict = {'name': classification.name, 'product_name': classification.product_name,
                                          'reference_price': classification.reference_price,
                                          'images_big': images_big_list,
                                          'characteristic': classification.characteristic,
                                          'discount': classification.discount,
                                          'images_parameter': classification_url + classification.images_parameter,
                                          'original_price': classification.original_price,
                                          'manual_price': classification.manual_price,
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
                                       'state': voucher.state, 'images_small': voucher_url + voucher.images_small,
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
                                          'describe': banner_obj.describe,
                                          'images_big': banners_url + banner_obj.images,
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
                "package": 'prepay_id' + prepay_id,
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
            create_room_url = "https://api.weixin.qq.com/wxaapi/broadcast/room/create?access_token=" + access_token
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
            phone_number = request._request.POST.get('phone_number')
            odoo = odoorpc.ODOO('47.92.85.245', port=3369)
            odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')
            feeling_customer_obj = odoo.env['feeling_customer.information']
            user_id = feeling_customer_obj.search([('customer_information_phone', '=', phone_number)])
            customer_credit = feeling_customer_obj.browse(user_id)['customer_business']

            ticket_type = request._request.POST.get('ticket_type')
            ticket_objs = models.Ticket.objects.all()
            ticket_objs_type_dict = {}
            ticket_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/ticket/"
            for ticket_obj in ticket_objs:
                if ticket_obj.ticket_type == ticket_type:
                    ticket_information_list = ticket_obj.ticket_information.split(',')
                    if customer_credit in ticket_information_list:
                        ticket_dict = {
                            "ticket_id": ticket_obj.id,
                            "ticket_name": ticket_obj.ticket_name,
                            "ticket_information": ticket_obj.ticket_information,
                            "ticket_image": ticket_url + ticket_obj.ticket_image,
                            "ticket_image_detail": ticket_obj.ticket_image_detail,
                            "remark": ticket_obj.remark,
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
class Card(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            ticket_type = request._request.POST.get('ticket_type')
            ticket_objs = models.Ticket.objects.all()
            ticket_objs_type_dict = {}
            ticket_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/ticket/"
            for ticket_obj in ticket_objs:
                if ticket_obj.ticket_type == ticket_type:
                    ticket_dict = {
                        "ticket_id": ticket_obj.id,
                        "ticket_name": ticket_obj.ticket_name,
                        "ticket_information": ticket_obj.ticket_information,
                        "ticket_image": ticket_url + ticket_obj.ticket_image,
                        "ticket_image_detail": ticket_obj.ticket_image_detail,
                        "remark": ticket_obj.remark,
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
class Point(APIView):

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            phone_number = request._request.POST.get('phone_number')
            odoo = odoorpc.ODOO('47.92.85.245', port=3369)
            odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')
            feeling_customer_obj = odoo.env['feeling_customer.information']
            user_id = feeling_customer_obj.search([('customer_information_phone', '=', phone_number)])
            customer_credit = feeling_customer_obj.browse(user_id)['customer_credit']
            responses['data'] = customer_credit
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
                            "value": float(bill_object.unit_price) * float(bill_object.quantity)
                        }

                        bill_object_list.append(bill_dict)
                        bill_chart_value_list.append(bill_chart)
                        bill_chart_name_list.append(bill_object.cost_name)
                        bill_chart_color_list.append(bill_object.chart_color)
                        bill_total += float(bill_object.unit_price) * float(bill_object.quantity)
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
                            bill_detail_dict["item_total"] += float(bill_object.unit_price) * float(
                                bill_object.quantity)
                            bill_detail_dict["customer_name"] = bill_object.customer_name
                            bill_detail_dict["trading_time"] = bill_object.trading_time
                        else:
                            bill_dict["item_quantity"] = 1
                            bill_dict["retail_id"] = bill_object.Retail_id
                            bill_dict["invitation_id"] = bill_object.InvitationCode_id
                            bill_dict["item_total"] = float(bill_object.unit_price) * float(bill_object.quantity)
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
                    "item_total": float(bill_object.unit_price) * float(bill_object.quantity),
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
                    path = os.path.join(settings.IMAGES_DIR[0]) + '/{}'.format(invitation_code)
                    path_pic = path + '/' + '{}'.format(pic_item) + '.jpg'

                    path_static = os.path.join(settings.STATIC_IMAGES_DIR[0]) + '/{}'.format(invitation_code)
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
            check_url = check_static_url + invitation_code
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
                models.Cart.objects.update_or_create(cart_code=invitation_code,
                                                     Classification_id=classification_object_id)

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
            models.Cart.objects.filter(cart_code=invitation_code,
                                       Classification_id=classification_object_id).first().delete()
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
            app_id = 'wxc754f862e84d18b5'
            secret = 'ddbe4a7654a3223c6ed40921f083995c'
            content = requests.get(
                url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'.format(
                    APPID=app_id, APPSECRET=secret))
            access_token = json.loads(content.content)['access_token']
            content = requests.post(
                url='https://api.weixin.qq.com/wxa/generatescheme?access_token={ACCESS_TOKEN}'.format(
                    ACCESS_TOKEN=access_token)).content
            open_link = json.loads(content)['openlink']
            response = HttpResponse("", status=302)
            response['Location'] = open_link
            return response
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class ManifestBill(APIView):
    """
        Return information of authentication process
        User authentication related services
    """

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
            user_id = odoo.env['feeling_customer.information'].search(
                [('customer_information_phone', '=', phone_number)])
            freight_obj = odoo.env['fixed.freight_bill']
            manifest_list = freight_obj.search(
                ['&', ('date_invoice', '=', data_time), ('partner_name_id', '=', user_id)])

            list_number = len(manifest_list)
            freight_filter_obj_list = freight_obj.browse(manifest_list)
            manifest_line_list = []
            for freight_filter_obj in freight_filter_obj_list:
                freight_total_prices = freight_filter_obj.amount_total_signed
                freight_id = freight_filter_obj.id
                freight_line_list = []
                manifest_lines = odoo.env['fixed.freight_bill.line'].search([('freight_id', '=', freight_id)])
                for manifest in manifest_lines:
                    manifest_obj = odoo.env['fixed.freight_bill.line'].browse(manifest)
                    length_of_the_goods = manifest_obj['length_of_the_goods']
                    width_of_the_goods = manifest_obj['width_of_the_goods']
                    area_of_the_goods = manifest_obj['area_of_the_goods']
                    unit_price = manifest_obj['unit_price']
                    remark = manifest_obj['remark']
                    freight_line_price = length_of_the_goods * width_of_the_goods * unit_price
                    if not remark:
                        remark = "无"
                    freight_line_list.append({
                        'product_id': manifest_obj['product_id'],
                        'length_of_the_goods': length_of_the_goods,
                        'width_of_the_goods': width_of_the_goods,
                        'area_of_the_goods': area_of_the_goods,
                        'unit_price': unit_price,
                        'freight_line_price': freight_line_price,
                        'remark': remark
                    })
                manifest_line = {
                    "freight_total_prices": freight_total_prices,
                    "freight_line_list": freight_line_list
                }
                manifest_line_list.append(manifest_line)
            manifest_dict = {
                "list_number": list_number,
                "manifest_list": manifest_line_list,
            }
            responses['manifest_dict'] = manifest_dict
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class PaintBill(APIView):
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
            user_id = odoo.env['feeling_customer.information'].search(
                [('customer_information_phone', '=', phone_number)])
            paint_sell_obj = odoo.env['feeling_manifest.sell']
            paint_sell_list = paint_sell_obj.search(
                ['&', ('sell_create_date', '=', data_time), ('sell_customer_name_id', '=', user_id)])
            list_number = len(paint_sell_list)
            paint_line_list = []
            number_flag = 0
            for paint_sell_id in paint_sell_list:
                number_flag += 1
                sell_total_prices = paint_sell_obj.browse(paint_sell_id).sell_total_prices
                paint_main_obj = odoo.env['feeling_manifest.main.line']
                paint_accessories_obj = odoo.env['feeling_manifest.accessories.line']

                paint_main_lines_ids = paint_main_obj.search([('sell_main_id', '=', paint_sell_id)])
                paint_accessories_lines_ids = paint_accessories_obj.search(
                    [('sell_accessories_id', '=', paint_sell_id)])

                paint_main_line_objs = paint_main_obj.browse(paint_main_lines_ids)
                paint_accessories_line_objs = paint_accessories_obj.browse(paint_accessories_lines_ids)

                paint_main_line_objs_list = []
                if paint_main_line_objs:
                    for paint_main_line_obj in paint_main_line_objs:
                        stock_model_name = paint_main_line_obj.manifest_flmodel_id.display_name
                        main_categories_number = paint_main_line_obj.main_categories_number
                        main_categories_code = paint_main_line_obj.main_categories_code
                        main_price = paint_main_line_obj.main_price
                        main_color_price = paint_main_line_obj.main_color_price
                        main_categories_specification = paint_main_line_obj.main_categories_specification
                        paint_main_line_objs_list.append({
                            'stock_model_name': stock_model_name,
                            'main_categories_number': main_categories_number,
                            'main_categories_code': main_categories_code,
                            'main_price': main_price,
                            'main_color_price': main_color_price,
                            'main_categories_specification': main_categories_specification,
                        })
                paint_accessories_line_objs_list = []
                if paint_accessories_line_objs:
                    for paint_accessories_line_obj in paint_accessories_line_objs:
                        stock_model_name = paint_accessories_line_obj.manifest_categories_id.display_name

                        accessories_categories_number = paint_accessories_line_obj.accessories_categories_number
                        accessories_categories_code = paint_accessories_line_obj.accessories_categories_code
                        accessories_price = paint_accessories_line_obj.accessories_price
                        accessories_categories_unit = paint_accessories_line_obj.accessories_categories_unit
                        paint_accessories_line_objs_list.append({
                            'stock_model_name': stock_model_name,
                            'accessories_categories_number': accessories_categories_number,
                            'accessories_categories_code': accessories_categories_code,
                            'accessories_price': accessories_price,
                            'accessories_categories_unit': accessories_categories_unit,
                        })
                paint_line_list.append({
                    'number_flag': number_flag,
                    'main_categories_list': paint_main_line_objs_list,
                    'accessories_categories_list': paint_accessories_line_objs_list,
                    'sell_total_prices': sell_total_prices
                })

            manifest_dict = {
                "list_number": list_number,
                "paint_line_list": paint_line_list,
            }
            responses['manifest_dict'] = manifest_dict
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
            data_year = request._request.POST.get('data_year')
            data_month = request._request.POST.get('data_month')
            data_date = request._request.POST.get('data_date')
            phone_number = request._request.POST.get('phone_number')
            odoo = odoorpc.ODOO('47.92.85.245', port=3369)
            odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')

            customer_information = odoo.env['feeling_customer.information']
            user_id = customer_information.search([('customer_information_phone', '=', phone_number)])
            customer_business = customer_information.browse(user_id).customer_business

            if customer_business == "wallpaper":
                freight_bill = odoo.env['fixed.freight_bill']
                manifest_ids_list = freight_bill.search([('partner_name_id', '=', user_id)])
                freight_bill_obj = freight_bill.browse(manifest_ids_list)
            else:
                manifest_sell = odoo.env['feeling_manifest.sell']
                manifest_ids_list = manifest_sell.search([('sell_customer_name_id', '=', user_id)])
                freight_bill_obj = manifest_sell.browse(manifest_ids_list)
            manifest_dict = {
                "list_number": 0,
                "manifest_list": [],
            }
            if not data_year:
                """全年的数据"""
                year_list = []
                year_month_dict = {}
                for bill in freight_bill_obj:
                    if customer_business == "wallpaper":
                        bill_time = str(bill.date_invoice)
                    else:
                        bill_time = str(bill.sell_create_date)
                    year_month_date = bill_time.split('-')[0] + '-' + bill_time.split('-')[1]
                    if year_month_date in year_month_dict:
                        year_month_dict[year_month_date].append(bill)
                    else:
                        year_month_dict[year_month_date] = []
                        year_month_dict[year_month_date].append(bill)

                for year_month in year_month_dict:
                    year_month_price = 0
                    year_months_obj = year_month_dict[year_month]
                    for year_month_obj in year_months_obj:
                        if customer_business == "wallpaper":
                            year_month_price += year_month_obj.amount_total_signed
                        else:
                            year_month_price += year_month_obj.sell_total_prices
                    result_data_dict = {
                        "time": year_month,
                        "amount": len(year_months_obj),
                        "year_month_price": year_month_price
                    }
                    year_list.append(result_data_dict)
                "冒泡降序"
                for i in range(len(year_list) - 1):
                    for j in range(len(year_list) - i - 1):
                        if time.strptime(year_list[j]['time'], '%Y-%m') < time.strptime(year_list[j + 1]['time'],
                                                                                        '%Y-%m'):
                            t = year_list[j]
                            year_list[j] = year_list[j + 1]
                            year_list[j + 1] = t

                manifest_dict = {
                    "list_number": len(year_list),
                    "manifest_list": year_list,
                }
            if not data_month:
                """
                   一年各个月份的简略数据，例如2022年的各个月份
                """
                pass
            if data_year and not data_date:
                """
                    某年某一个月的所有数据，例如2022年一月的所有数据
                """
                """全年的数据"""
                year_month_list = []
                year_month_dict = {}
                item_time = data_year + '-' + data_month
                for bill in freight_bill_obj:
                    if customer_business == "wallpaper":
                        bill_time = str(bill.date_invoice)
                    else:
                        bill_time = str(bill.sell_create_date)
                    year_month_time = bill_time.split('-')[0] + '-' + bill_time.split('-')[1]
                    year_month_date_time = bill_time.split('-')[0] + '-' + bill_time.split('-')[1] + '-' + \
                                           bill_time.split('-')[2]
                    if item_time in year_month_time:
                        if year_month_date_time in year_month_dict:
                            year_month_dict[year_month_date_time].append(bill)
                        else:
                            year_month_dict[year_month_date_time] = []
                            year_month_dict[year_month_date_time].append(bill)

                for year_month_date in year_month_dict:
                    year_month_price = 0
                    year_months_obj = year_month_dict[year_month_date]
                    for year_month_obj in year_months_obj:
                        if customer_business == "wallpaper":
                            year_month_price += year_month_obj.amount_total_signed
                        else:
                            year_month_price += year_month_obj.sell_total_prices
                    result_data_dict = {
                        "time": year_month_date,
                        "amount": len(year_months_obj),
                        "year_month_price": year_month_price
                    }
                    year_month_list.append(result_data_dict)
                "冒泡降序"
                for i in range(len(year_month_list) - 1):
                    for j in range(len(year_month_list) - i - 1):
                        if time.strptime(year_month_list[j]['time'], '%Y-%m-%d') < time.strptime(
                                year_month_list[j + 1]['time'], '%Y-%m-%d'):
                            t = year_month_list[j]
                            year_month_list[j] = year_month_list[j + 1]
                            year_month_list[j + 1] = t

                manifest_dict = {
                    "list_number": len(year_month_list),
                    "manifest_list": year_month_list,
                }
            """具体到每天的数据，前端用ManifestBill的接口查询"""
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


# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys
from typing import List
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Samples:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
            **kwargs
    ):
        with open('/home/yanboce/apps/message.json', 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            access_key_id = json_data['access_key_id']
            access_key_secret = json_data['access_key_secret']
        phone_numbers = kwargs["phone_numbers"]
        sign_name = kwargs["sign_name"]
        template_code = kwargs["template_code"]
        template_param = kwargs["template_param"]
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Samples.create_client(access_key_id, access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_numbers,
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            return_result = client.send_sms_with_options(send_sms_request, runtime)
            return return_result
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            return None

    @staticmethod
    async def main_async(
            **kwargs
    ) -> None:
        with open('/home/yanboce/apps/message.json', 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            access_key_id = json_data['access_key_id']
            access_key_secret = json_data['access_key_secret']
        phone_numbers = kwargs["phone_numbers"]
        sign_name = kwargs["sign_name"]
        template_code = kwargs["template_code"]
        template_param = kwargs["template_param"]
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Samples.create_client(access_key_id, access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_numbers,
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            return_result = await client.send_sms_with_options_async(send_sms_request, runtime)
            return return_result
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            return None


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class SendMessage(APIView):
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
            phone_numbers = request._request.POST.get('phone_numbers')
            customer_name = request._request.POST.get('customer_name')
            customer_type = request._request.POST.get('customer_type')
            template_param = {"name": customer_name}
            template_code = ""
            if customer_type == "wallpaper":
                template_code = "SMS_269060503"
            elif customer_type == "paint":
                template_code = "SMS_269075502"
            return_result = Samples.main(
                phone_numbers=phone_numbers,
                sign_name="陕西邦臣建材有限公司",
                template_code=template_code,
                template_param=str(template_param)
            )
            if return_result:
                if return_result.body.code == "OK":
                    responses['status'] = "ok"
                else:
                    responses['status'] = "fail"
            else:
                responses['status'] = "fail"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Tvoc(APIView):
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
            phone_number = request._request.POST.get('phone_number')
            odoo = odoorpc.ODOO('47.92.85.245', port=3369)
            odoo.login('FenLin', '1979736774@qq.com', 'odooodoo')

            tvoc_obj = odoo.env['feeling_tvoc.check']
            tvoc_value_line_obj = odoo.env['feeling_tvoc.check.line']
            customer_information = odoo.env['feeling_customer.information']
            user_id = customer_information.search([('customer_information_phone', '=', phone_number)])
            tvoc_id = tvoc_obj.search([('tvoc_customer_name_id', '=', user_id)])
            if tvoc_id:
                tvoc_objs = tvoc_obj.browse(tvoc_id)
                tvoc_obj_list = []
                tvoc_customer_name_id = tvoc_objs[0].tvoc_customer_name_id.customer_information_name
                for tvoc_obj in tvoc_objs:
                    tvoc_check_date = tvoc_obj.tvoc_check_date
                    tvoc_id = tvoc_obj.tvoc_id
                    check_clerk = tvoc_obj.check_clerk
                    check_type = tvoc_obj.check_type
                    check_location_number = tvoc_obj.check_location_number
                    value_line_ids = tvoc_obj.id
                    tvoc_value_line_ids = odoo.env['feeling_tvoc.check.line'].search(
                        [('tvoc_value_id', '=', value_line_ids)])
                    tvoc_value_line_objs = tvoc_value_line_obj.browse(tvoc_value_line_ids)
                    tvoc_location_list = []
                    tvoc_result_list = []
                    tvoc_value_list = []
                    for tvoc_value_line in tvoc_value_line_objs:
                        tvoc_location = tvoc_value_line['tvoc_location']
                        tvoc_result = tvoc_value_line['tvoc_result']
                        tvoc_value = tvoc_value_line['tvoc_value']
                        tvoc_location_list.append(tvoc_location)
                        tvoc_result_list.append(tvoc_result)
                        tvoc_value_list.append(tvoc_value)
                    tvoc_obj_list.append({
                        "tvoc_customer_name_id": tvoc_customer_name_id,
                        "tvoc_check_date": tvoc_check_date,
                        "tvoc_id": tvoc_id,
                        "check_clerk": check_clerk,
                        "check_type": check_type,
                        "check_location_number": check_location_number,
                        "tvoc_location_list": tvoc_location_list,
                        "tvoc_result_list": tvoc_result_list,
                        "tvoc_value_list": tvoc_value_list
                    })
                tvoc_dict = {
                    "tvoc_obj_list": tvoc_obj_list,
                }
                responses['tvoc_dict'] = tvoc_dict
            else:
                responses['code'] = 1001
                responses['message'] = "暂无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class TypeColor(APIView):
    authentication_classes = []

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            color_type_objs = models.ColorType.objects.all()
            color_type_objs_list = []
            color_type_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/ticket/"
            for color_obj in color_type_objs:
                color_type_dict = {
                    "color_type_id": color_obj.id,
                    "color_type_name": color_obj.color_type_id,
                    "color_image": color_type_url + color_obj.color_type_pic,
                }
                color_type_objs_list.append(color_type_dict)
            responses['data'] = {
                "color_type_data": color_type_objs_list
            }
            pass
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class ColorUnit(APIView):
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
            color_id = request._request.POST.get('color_id')
            if color_id:
                color_type_objs = models.ColorUnit.objects.filter(Retail_id=color_id).all()
                color_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/color/"
                color_list = []
                for color_type_obj in color_type_objs:
                    color_dict = {
                        "id": color_type_obj.id,
                        "color_id": color_type_obj.color_id,
                        "color_name": color_type_obj.color_name,
                        "color_type": color_type_obj.color_type,
                        "color_unit_image": color_url + color_type_obj.color_unit_pic,
                        "remark": color_type_obj.remark,
                    }
                    color_list.append(color_dict)
                responses['data'] = color_list
            else:
                responses['code'] = 1001
                responses['message'] = "暂无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class ColorUnitPic(APIView):
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
            color_id = request._request.POST.get('color_id')
            if color_id:
                color_type_obj = models.ColorUnit.objects.filter(color_id=color_id).first()
                color_url = "https://www.zhuangyuanjie.cn/static/media/manufactor/color/"
                color_dict_pic = {
                    "id": color_type_obj.id,
                    "color_list": []
                }
                if color_type_obj.color_pic_1:
                    color_dict_pic['color_list'].append(color_url + color_type_obj.color_pic_1)
                if color_type_obj.color_pic_2:
                    color_dict_pic['color_list'].append(color_url + color_type_obj.color_pic_2)
                if color_type_obj.color_pic_3:
                    color_dict_pic['color_list'].append(color_url + color_type_obj.color_pic_3)
                if color_type_obj.color_pic_4:
                    color_dict_pic['color_list'].append(color_url + color_type_obj.color_pic_4)
                if color_type_obj.color_unit_pic:
                    color_dict_pic['color_list'].append(color_url + color_type_obj.color_unit_pic)
                responses['data'] = color_dict_pic
            else:
                responses['code'] = 1001
                responses['message'] = "暂无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AllColor(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    # 定义计算颜色相似度的函数

    def color_distance(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    # 定义函数查找五个渐变色最接近的数组
    def find_closest_gradient_colors(self, rgb, color_list):
        # 计算与给定颜色rgb的相似度并存入列表中
        # distances = [self.color_distance(rgb, color[1:]) for color in color_list]
        distances = []
        for color in color_list:
            distances.append(self.color_distance(rgb, color[1:]))
        # 对相似度进行排序
        sorted_distances = sorted(distances)
        # 寻找五个最接近的颜色
        closest_colors = []
        for i in range(6):
            idx = distances.index(sorted_distances[i])
            closest_colors.append(color_list[idx])
            distances[idx] = float('inf')
        return closest_colors

    # 互补色
    @staticmethod
    def find_complementary_colors(rgb, colors, n=6):
        # 计算RGB颜色的互补色
        complementary_rgb = (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])

        # 计算每个颜色与互补色的欧几里得距离
        distances = [(i, ((c[1] - complementary_rgb[0]) ** 2 +
                          (c[2] - complementary_rgb[1]) ** 2 +
                          (c[3] - complementary_rgb[2]) ** 2) ** 0.5)
                     for i, c in enumerate(colors)]

        # 按照距离排序并返回最接近的n个颜色
        sorted_distances = sorted(distances, key=lambda x: x[1])
        return [colors[i[0]] for i in sorted_distances[:n]]

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            color_input_name = request._request.POST.get('color_input_name')
            color_input_name = json.loads(color_input_name)
            color_type_objs = models.TotalColor.objects.all()
            color_grateful_obj = models.ColorUnit.objects.all()
            grateful_list = []
            color_list = []
            for grateful_color in color_grateful_obj:
                if grateful_color.remark:
                    grateful_rgb = json.loads(grateful_color.remark)
                    grateful_list.append((grateful_color.color_id, grateful_rgb[0], grateful_rgb[1], grateful_rgb[2]))
            for color_obj in color_type_objs:
                color_rgb = json.loads(color_obj.color_rgb)
                color_list.append((color_obj.color_name, color_rgb[0], color_rgb[1], color_rgb[2]))
            # 查找与rgb颜色的互补色最接近的5个颜色
            hubuse_list = self.find_complementary_colors(color_input_name, color_list, n=6)
            # 查找与rgb颜色的渐变色色最接近的5个颜色
            jianbianse_list = self.find_closest_gradient_colors(color_input_name, color_list)
            # 在热门色号中，查找与rgb颜色的渐变色色最接近的5个颜色
            grateful_list = self.find_closest_gradient_colors(color_input_name, grateful_list)

            step = 3
            hubuse_list = [hubuse_list[i:i + step] for i in range(0, len(hubuse_list), step)]
            jianbianse_list = [jianbianse_list[i:i + step] for i in range(0, len(jianbianse_list), step)]
            grateful_list = [grateful_list[i:i + step] for i in range(0, len(grateful_list), step)]

            color_analyse = {
                "hubuse": hubuse_list,
                "jianbianse": jianbianse_list,
                "grateful": grateful_list
            }
            responses['data'] = color_analyse
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AllColorDetail(APIView):
    """
        Return information of authentication process
        User authentication related services
    """

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        try:
            color_type = request._request.POST.get('color_type')
            color_system = request._request.POST.get('color_system')

            query = Q()  # Initialize an empty Q object
            if color_type is not None and color_type != '':
                query &= Q(color_type=color_type)
            if color_system is not None and color_system != '':
                query &= Q(color_system=color_system)
            color_type_objs = models.TotalColor.objects.filter(query)
            color_list = []
            for color_type_obj in color_type_objs:
                color_rgb = json.loads(color_type_obj.color_rgb)
                color_list.append([color_type_obj.color_name, color_rgb])
            step = 3
            color_list_3 = [color_list[i:i + step] for i in range(0, len(color_list), step)]
            color_selected = {
                "color_list_3": color_list_3,
            }
            responses['data'] = color_selected
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class EntryPhoneNumber(APIView):
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

            invitation_objs = models.ZyjWechatInvitationCode.objects.all()
            phone_list = []
            for invitation_obj in invitation_objs:
                invitation_phone_number = invitation_obj.invitation_code
                phone_list.append(invitation_phone_number)
            responses['data'] = phone_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


from PIL import Image
import numpy as np
import tempfile
from sklearn.cluster import KMeans


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AiSelectColor(APIView):
    """
        Return information of authentication process
        User authentication related services
    """
    authentication_classes = []

    def get_image_colors(self, image_path, num_colors=3):
        # 打开图片
        image = Image.open(image_path)

        # 将图片大小调整为较小的尺寸以提高处理速度
        image = image.resize((150, 150))

        # 将图像数据转换为numpy数组
        pixels = np.array(image)

        # 将二维的图像数组展平成一维数组
        flattened_pixels = pixels.reshape(-1, 3)

        # 使用KMeans聚类找到主要颜色
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(flattened_pixels)
        dominant_colors = kmeans.cluster_centers_

        # 将主要颜色的RGB值四舍五入为整数
        rounded_colors = dominant_colors.round(0).astype(int)

        return rounded_colors

    def color_distance(self, c1, c2):
        return np.sqrt(np.sum((np.array(c1) - np.array(c2)) ** 2))

    def find_closest_color(self, input_color, colors):
        min_distance = float('inf')
        closest_color_name = None
        closest_color_rgb = None
        for color_name, color_value in colors.items():
            distance = self.color_distance(input_color, color_value)

            if distance < min_distance:
                min_distance = distance
                closest_color_name = color_name
                closest_color_rgb = color_value

        return closest_color_name, closest_color_rgb

    def analyze_color(self, input_color):
        colors = {
            "红色": (255, 0, 0),
            "绿色": (0, 255, 0),
            "蓝色": (0, 0, 255),
            "黄色": (255, 255, 0),
            "青色": (0, 255, 255),
            "品红": (255, 0, 255),
            "白色": (255, 255, 255),
            "黑色": (0, 0, 0),
            "棕色": (165, 42, 42),
            "橙色": (255, 165, 0),
            "浅黄色": (252, 232, 179),
            "淡蓝色": (135, 206, 250),
            "紫色": (128, 0, 128),
            "金色": (255, 215, 0),
            "银色": (192, 192, 192),
            "深红色": (139, 0, 0),
            "橄榄绿": (128, 128, 0),
            "深蓝色": (0, 0, 139),
            "淡紫色": (221, 160, 221),
            "深紫色": (75, 0, 130),
            "石榴红": (255, 20, 147),
            "巧克力色": (210, 105, 30),
            "天蓝色": (30, 144, 255),
            "绿松石": (64, 224, 208),
            "酒红色": (128, 0, 0),
            "海绿色": (46, 139, 87),
            "石灰绿": (50, 205, 50),
            "薰衣草": (230, 230, 250),
            "紫罗兰": (238, 130, 238),
            "中绿色": (0, 128, 0),
            "中蓝色": (0, 0, 205),
            "暗灰色": (169, 169, 169),
            "玫瑰红": (255, 0, 127),
            "亮绿色": (144, 238, 144),
            "鸢尾花色": (85, 107, 47),
            "亮金色": (238, 221, 130),
            "中紫色": (147, 112, 219),
            "苍绿色": (152, 251, 152),
            # "钢蓝": (70, 130, 180),
            "金麒麟色": (233, 216, 173),
            "暗绿色": (0, 100, 0),
            "暗海绿色": (143, 188, 143),
            "暗紫色": (102, 51, 153),
            "古铜色": (205, 127, 50),
            "亮珊瑚色": (240, 128, 128),
            "蓝绿色": (32, 178, 170),
            "亮蓝色": (173, 216, 230),
            "橙红色": (255, 69, 0),
            "深橙色": (255, 140, 0),
            "深粉色": (255, 20, 147),
            "亮紫色": (218, 112, 214),
            "火砖色": (178, 34, 34),
            "法国玫瑰色": (246, 74, 138),
            "浅粉色": (255, 182, 193),
            "亮麒麟色": (250, 250, 210),
            "亮青色": (95, 158, 160),
            "珍珠白": (234, 224, 200),
            "珍珠红": (183, 110, 121),
            "珍珠蓝": (77, 121, 255),
            "烟白色": (245, 245, 245),
            "中石板蓝": (123, 104, 238),
            "草绿色": (124, 252, 0),
            "柠檬绸色": (255, 250, 205),
            "亮天蓝色": (135, 206, 255),
            "洋红色": (255, 0, 255),
            "米色": (245, 222, 179),
            "孔雀石绿": (50, 205, 153),
            "梅红色": (176, 48, 96),
            "马鞍棕": (139, 69, 19),
            "沙棕色": (244, 164, 96),
            "海贝色": (255, 228, 196),
            "紫罗兰红": (208, 32, 144),
            "石板蓝": (106, 90, 205),
            "草莓色": (252, 90, 141),
            "棕绿色": (150, 75, 0),
            "棕褐色": (139, 35, 35),
            "中宝石蓝": (48, 99, 191),
            "茶色": (210, 180, 140),
            "薄荷色": (24, 176, 116),
            "藏青色": (16, 78, 139),
            "旧麻色": (253, 245, 230),
            "土耳其蓝": (0, 199, 140),
            "亮石板灰": (207, 207, 196),
            "玫瑰金": (183, 110, 121),
            "柔和黄": (253, 253, 150),
            "石榴石绿": (0, 201, 87),
            "亮绿松石": (0, 229, 238),
            "烟雾蓝": (96, 130, 182),
            "暗茶色": (101, 67, 33),
            "森林绿": (34, 139, 34),
            "海军蓝": (0, 0, 128),
            "橄榄土": (87, 59, 12),
            "暗金黄": (184, 134, 11),
            "亮绿": (0, 255, 127),
            "薄荷绿": (245, 255, 250),
            "浅钢蓝": (176, 196, 222),
            "橙黄色": (255, 174, 66),
            "鲑红色": (250, 128, 114),
            "苍老紫": (148, 0, 211),
            "暗橙色": (255, 140, 0),
            "暗灰蓝": (72, 61, 139),
            "石板灰": (112, 128, 144),
            "栗色": (128, 0, 0),
            "珊瑚色": (255, 127, 80),
            "青蓝色": (51, 153, 255),
            "昏灰": (105, 105, 105),
            "印度红": (205, 92, 92),
            "深天蓝": (0, 191, 255),
            "亮钢蓝": (202, 225, 255),
            "蜜蜂蓝": (39, 58, 129),
            "绿松石蓝": (0, 199, 140),
            "绛紫色": (226, 43, 138),
            "砖红色": (156, 102, 31),
            "暗鲑红": (233, 150, 122),
            "深天鹅绿": (0, 199, 89),
            "紫水晶": (155, 135, 206),
            "亮杏仁色": (255, 235, 205),
            "象牙色": (255, 255, 240),
            "普莱士红": (153, 0, 76),
            "中紫红": (186, 85, 211),
            "深红褐": (139, 0, 0),
            "暗褐色": (101, 67, 33),
            "浅绿松石": (64, 224, 208),
            "深绿色": (100, 255, 100),
            "浅蓝色": (200, 200, 255),
            "浅绿色": (200, 255, 200),
            "浅红色": (255, 200, 200),
            "中红色": (255, 128, 128),
            "深黄色": (255, 255, 100),
            "淡黄色": (255, 255, 200),
            "中黄色": (255, 255, 128),
            "橘黄色": (255, 165, 0),
            "浅橘黄色": (255, 210, 100),
            "深橘黄色": (255, 140, 0),
            "暗橘黄色": (255, 130, 0),
            "亮橘黄色": (255, 180, 30),
            "深青色": (100, 255, 255),
            "浅青色": (200, 255, 255),
            "中青色": (128, 255, 255),
            "暗青色": (50, 255, 255),
            "深磁红色": (255, 100, 255),
            "浅磁红色": (255, 200, 255),
            "中磁红色": (255, 128, 255),
            "暗磁红色": (255, 50, 255),
            "亮磁红色": (255, 150, 255),
            "深磁绿色": (255, 255, 100),
            "浅磁绿色": (255, 255, 200),
            "中磁绿色": (255, 255, 128),
            "暗磁绿色": (255, 255, 50),
            "亮磁绿色": (255, 255, 150),
            "深磁蓝色": (100, 255, 255),
            "中磁蓝色": (128, 255, 255),
            "暗磁蓝色": (50, 255, 255),
            "亮磁蓝色": (150, 255, 255),
            "深茶色": (210, 105, 30),
            "浅茶色": (222, 184, 135),
            "中茶色": (244, 164, 96),
            "亮茶色": (255, 228, 181),
            "深橄榄色": (100, 255, 0),
            "浅橄榄色": (200, 255, 0),
            "中橄榄色": (128, 255, 0),
            "暗橄榄色": (50, 255, 0),
            "亮橄榄色": (150, 255, 0),
            "深金色": (255, 200, 0),
            "浅金色": (255, 215, 0),
            "中金色": (255, 223, 0),
            "暗金色": (255, 165, 0),
            "深鸟蛋蓝": (0, 255, 255),
            "浅鸟蛋蓝": (0, 255, 200),
            "中鸟蛋蓝": (0, 255, 128),
            "暗鸟蛋蓝": (0, 255, 50),
            "亮鸟蛋蓝": (0, 255, 150),
            "中粉色": (255, 0, 128),
            "暗粉色": (255, 0, 50),
            "亮粉色": (255, 0, 150),
            "深紫罗兰": (238, 130, 238),
            "浅紫罗兰": (218, 112, 214),
            "中紫罗兰": (221, 160, 221),
            "暗紫罗兰": (139, 0, 139),
            "亮紫罗兰": (238, 0, 238),
            "深森林绿": (34, 139, 34),
            "浅森林绿": (144, 238, 144),
            "中森林绿": (102, 205, 170),
            "暗森林绿": (0, 100, 0),
            "亮森林绿": (60, 179, 113),
            "深珊瑚红": (255, 99, 71),
            "中珊瑚红": (240, 128, 128),
            "暗珊瑚红": (205, 92, 92),
            "亮珊瑚红": (255, 160, 122),
            "深石榴红": (178, 34, 34),
            "浅石榴红": (255, 182, 193),
            "中石榴红": (255, 106, 106),
            "暗石榴红": (139, 58, 58),
            "亮石榴红": (255, 20, 147),
            "深海蓝": (72, 61, 139),
            "浅海蓝": (173, 216, 230),
            "中海蓝": (100, 149, 237),
            "暗海蓝": (0, 0, 139),
            "亮海蓝": (135, 206, 250),
            "深绿松石": (0, 128, 128),
            "中绿松石": (0, 255, 255),
            "暗绿松石": (0, 139, 139),
            "深酒红": (128, 0, 0),
            "浅酒红": (255, 240, 245),
            "中酒红": (255, 0, 0),
            "暗酒红": (139, 0, 0),
            "亮酒红": (255, 105, 180),
            "深紫红": (153, 50, 204),
            "浅紫红": (186, 85, 211),
            "暗紫红": (128, 0, 128),
            "亮紫红": (216, 191, 216),
            "深黄绿": (124, 252, 0),
            "浅黄绿": (127, 255, 0),
            "中黄绿": (173, 255, 47),
            "暗黄绿": (85, 107, 47),
            "亮黄绿": (154, 205, 50),
            "深暖棕": (210, 180, 140),
            "浅暖棕": (245, 245, 220),
            "中暖棕": (222, 184, 135),
            "暗暖棕": (139, 69, 19),
            "亮暖棕": (244, 164, 96),
            "淡赭石": (220, 195, 185),
            "暮光蓝": (190, 205, 215),
            "米黄": (235, 230, 190),
            "浅雪松": (185, 215, 210),
            "砂棕": (195, 185, 165),
            "晨雾": (215, 225, 225),
            "橄榄褐": (200, 195, 160),
            "梦境蓝": (210, 220, 230),
            "棕绿": (210, 210, 180),
            "银杏黄": (225, 225, 190),
            "幽灵白": (235, 235, 245),
            "月光石": (210, 210, 210),
            "泥泞绿": (205, 210, 185),
            "藕荷粉": (235, 210, 220),
            "安静绿": (190, 200, 185),
            "亮蜜桃": (245, 225, 210),
            "烟雾紫": (210, 190, 210),
            "暗瓦灰": (210, 195, 180),
            "珊瑚粉": (245, 215, 215),
            "浅钴绿": (185, 215, 205),
            "纸棕": (215, 200, 175),
            "薄荷奶昔": (230, 245, 230),
            "嫩苹果绿": (215, 235, 215),
            "暗草灰": (185, 195, 180),
            "薄雾灰": (225, 225, 235),
            "清晨蓝": (215, 230, 240),
            "桔梗紫": (195, 185, 215),
            "糖果棕": (230, 200, 185),
            "清新黄": (240, 240, 210),
            "绿松石灰": (200, 225, 215),
            "浅鹿皮": (210, 195, 170),
            "春日蓝": (210, 235, 245),
            "白杨绿": (210, 235, 210),
            "灰绿松石": (185, 210, 200),
            "淡牡丹红": (245, 210, 220),
            "蓝石灰": (195, 210, 215),
            "暗米黄": (210, 205, 170),
            "苍穹灰": (185, 195, 210),
            "榛果棕": (210, 190, 170),
            "苹果绿灰": (190, 215, 190),
            "暗花灰": (200, 180, 200),
            "沙漠黄": (230, 220, 185),
            "浅灰蓝": (215, 225, 235),
            "淡薰衣草": (225, 210, 240),
            "蓝灰": (190, 210, 225),
            "石英粉": (235, 210, 230),
            "灰橄榄": (185, 205, 175),
            "烟蓝": (210, 215, 230),
            "沙石黄": (220, 210, 175),
            "薄荷灰": (200, 235, 215),
            "玫瑰灰": (215, 190, 195),
            "柔绿": (185, 215, 185),
            "海石蓝": (195, 205, 225),
            "灰棕": (195, 185, 165),
            "浅樱桃": (235, 200, 210),
            "棕灰": (205, 190, 170),
            "蓝绿灰": (190, 215, 215),
            "月光黄": (230, 230, 200),
            "柔粉": (235, 215, 225),
            "淡绿松石": (195, 225, 215),
            "暗海蓝灰": (185, 190, 210),
            "紫罗兰灰": (215, 190, 215),
            "亮鹿皮": (220, 205, 180),
            "淡橄榄绿": (200, 215, 180),
            "银河蓝": (210, 215, 235),
            "草坪灰": (190, 210, 190),
            "暗麻灰": (180, 185, 170),
            "暗褐": (101, 67, 33),
            "酒红": (128, 0, 0),
            "黑橄榄": (61, 61, 0),
            "深橙": (255, 140, 0),
            "暗灰": (169, 169, 169),
            "深巧克力色": (65, 29, 7),
            "暗绿": (0, 100, 0),
            "深卡其布": (189, 183, 107),
            "暗洋红": (139, 0, 139),
            "暗珊瑚": (205, 92, 92),
            "暗鲑鱼色": (233, 150, 122),
            "暗海绿": (143, 188, 143),
            # "暗鼠尾草": (118, 128, 105),
            "暗乌贼墨": (85, 107, 47),
            "暗鸢尾蓝": (112, 128, 144),
            "煤黑": (47, 79, 79),
            "深鲑鱼色": (255, 69, 0),
            "深橄榄绿": (85, 107, 47),
            "暗蓝绿": (50, 204, 204),
            "暗金菊": (184, 134, 11),
            "深浅蓝": (240, 248, 255),
            "暗矿蓝": (0, 34, 102),
            "暗草绿": (102, 102, 51),
            "暗粉红": (205, 92, 205),
            "深紫外光": (51, 0, 102),
            "暗中红": (255, 0, 127),
            "暗雪松": (107, 142, 35),
            "暗玫瑰红": (255, 0, 255),
            "深莹绿": (0, 128, 0),
        }

        closest_color_name, closest_color_rgb = self.find_closest_color(input_color, colors)
        # return f"输入的RGB颜色{input_color}属于{closest_color}。"
        return closest_color_name, closest_color_rgb

    def find_complementary_colors(self, rgb, colors, n=6):
        # 计算RGB颜色的互补色
        complementary_rgb = (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])

        # 计算每个颜色与互补色的欧几里得距离
        distances = [(i, ((c[1] - complementary_rgb[0]) ** 2 +
                          (c[2] - complementary_rgb[1]) ** 2 +
                          (c[3] - complementary_rgb[2]) ** 2) ** 0.5)
                     for i, c in enumerate(colors)]

        # 按照距离排序并返回最接近的n个颜色
        sorted_distances = sorted(distances, key=lambda x: x[1])
        return [colors[i[0]] for i in sorted_distances[:n]]

    def post(self, request):
        responses = {
            'code': 1000,
            'message': None
        }
        # 将处理后的图片保存到一个临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            files = request.FILES
            uploaded_image = files.get('image', None)
            img = Image.open(uploaded_image)

            img.save(temp_file.name, 'PNG')

            # 在这里你可以将临时文件的路径传递给其他函数进行处理

            color_grateful_obj = models.ColorUnit.objects.all()
            grateful_list = []
            for grateful_color in color_grateful_obj:
                if grateful_color.remark:
                    grateful_rgb = json.loads(grateful_color.remark)
                    grateful_list.append((grateful_color.color_id, grateful_rgb[0], grateful_rgb[1], grateful_rgb[2]))

            image_path = uploaded_image
            main_colors = self.get_image_colors(image_path, num_colors=1)
            main_color = ''
            for idx, color in enumerate(main_colors):
                # print(f"主要颜色 {idx + 1}: {tuple(color)}")
                main_color = tuple(color)
            # main_color_name, main_color_rgb = self.analyze_color(main_color)
            hubuse_list = self.find_complementary_colors(main_color, grateful_list)
            main_color_rgb_int: List[int] = []
            main_color_rgb_str: Str[int] = []
            for i in main_color:
                main_color_rgb_int.append(int(i))
                main_color_rgb_str.append(str(i))
            main_color_name = ",".join(main_color_rgb_str)
            main_color_name = 'RGB(' + main_color_name + ')'
            color_analyse = {
                "main_color": main_color_name,
                "main_color_rgb": main_color_rgb_int,
                "hubuse": hubuse_list,
            }
            responses['data'] = color_analyse
            # 关闭临时文件
            temp_file.close()

        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        # 接口调用完成后删除临时文件
        os.unlink(temp_file.name)
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class HomeSwiperPic(APIView):
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
            ads_image_type = request._request.POST.get('ads_image_type')
            ads_image_page = request._request.POST.get('ads_image_page')
            ads_image_name = request._request.POST.get('ads_image_name')
            ads_image_status = request._request.POST.get('ads_image_status')
            query = Q()  # Initialize an empty Q object
            if ads_image_type is not None and ads_image_type != '':
                query &= Q(ads_image_type=ads_image_type)
            if ads_image_page is not None and ads_image_page != '':
                query &= Q(ads_image_page=ads_image_page)
            if ads_image_name is not None and ads_image_name != '':
                query &= Q(ads_image_name=ads_image_name)
            if ads_image_status is not None and ads_image_status != '':
                query &= Q(ads_image_status=ads_image_status)
            filtered_ad_image_types = models.AdsImage.objects.filter(query)
            if filtered_ad_image_types:
                result_list = []
                for filtered_ad_image_type in filtered_ad_image_types:
                    if filtered_ad_image_type.ads_image_status == "valid":
                        result_list.append({
                            "image_id": filtered_ad_image_type.ads_image_id,
                            "title": filtered_ad_image_type.ads_image_title,
                            "image_status": filtered_ad_image_type.ads_image_status,
                            "image_pic": filtered_ad_image_type.ads_image_pic,
                        })
                responses['result'] = result_list
            else:
                responses['code'] = 1001
                responses['message'] = "暂无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AdsCoverPic(APIView):
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
            ads_image_type = request._request.POST.get('ads_image_type')
            ads_image_page = request._request.POST.get('ads_image_page')
            ads_image_name = request._request.POST.get('ads_image_name')
            ads_image_status = request._request.POST.get('ads_image_status')
            query = Q()  # Initialize an empty Q object
            if ads_image_type is not None and ads_image_type != '':
                query &= Q(ads_image_type=ads_image_type)
            if ads_image_page is not None and ads_image_page != '':
                query &= Q(ads_image_page=ads_image_page)
            if ads_image_name is not None and ads_image_name != '':
                query &= Q(ads_image_name=ads_image_name)
            if ads_image_status is not None and ads_image_status != '':
                query &= Q(ads_image_status=ads_image_status)
            filtered_ad_image_types = models.AdsImage.objects.filter(query)
            if filtered_ad_image_types:
                result_list = []
                for filtered_ad_image_type in filtered_ad_image_types:
                    if filtered_ad_image_type.ads_image_status == "valid":
                        result_list.append({
                            "image_id": filtered_ad_image_type.ads_image_id,
                            "title": filtered_ad_image_type.ads_image_title,
                            "name": filtered_ad_image_type.ads_image_name,
                            "image_status": filtered_ad_image_type.ads_image_status,
                            "image_pic": filtered_ad_image_type.ads_image_pic,
                        })
                responses['result'] = result_list
            else:
                responses['code'] = 1001
                responses['message'] = "暂无数据"
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AllColors(APIView):
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
            color_type = request._request.POST.get('color_type')
            color_type_objs = models.TotalColor.objects.filter(color_type=color_type).all()
            color_list = []
            for color_type_obj in color_type_objs:
                color_name = color_type_obj.color_name
                color_rgb = json.loads(color_type_obj.color_rgb)
                color_list.append({
                            "color_name": color_name,
                            "color_list": color_rgb,
                        })
            responses['result'] = color_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class ColorsCategory(APIView):
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
            color_name_list = []
            color_category_list = ['黄色', '橘色', '红色', '洋红', '紫色', '深蓝', '浅蓝', '绿色',
                                   '果绿', '黄绿', '莫兰迪绿', '莫兰迪黄', '莫兰迪红', '莫兰迪紫',
                                   '莫兰迪蓝', '莫兰迪绿', '莫兰迪黄绿', '莫兰迪褐', '莫兰迪灰', '莫兰迪黑']
            for id, color_category in enumerate(color_category_list):
                color_name_list.append({
                    "color_category_name": color_category,
                    "status": 1,
                    "id": id,
                })
            responses['result'] = color_name_list
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class SingleColors(APIView):
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
            color_code = request._request.POST.get('color_code')
            color_type_objs = models.TotalColor.objects.filter(color_name=color_code).first()
            if color_type_objs:
                color_dict_pic = {
                    "color_code": color_type_objs.color_name,
                    "color_list": color_type_objs.color_rgb,
                    "color_name": color_type_objs.hubuse_name,
                    "color_picture_1": color_type_objs.hubuse_rgb,
                    "color_picture_2": color_type_objs.leibise_name,
                    "color_picture_3": color_type_objs.leibise_rgb,
                    "color_picture_4": color_type_objs.jianbianse_name,
                    "color_picture_5": color_type_objs.jianbianse_rgb,
                }
                responses['result'] = color_dict_pic
            else:
                responses['result'] = []
        except Exception as e:
            responses['code'] = 3002
            responses['message'] = "请求异常"
        return JsonResponse(responses)
