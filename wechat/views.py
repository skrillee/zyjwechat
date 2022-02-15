__author__ = 'Yan.zhe 2021.09.28'

from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse
from zyjwechat import settings
from wechat import models
import socket
import datetime
import hashlib
import time
import pytz
import os
import json


def md5(invitation_code) -> object:
    current_time = str(time.time())
    md5_object = hashlib.md5(bytes(invitation_code, encoding='utf-8'))
    md5_object.update(bytes(current_time, encoding='utf-8'))
    return md5_object.hexdigest()


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
            invitation_code_object = models.ZyjWechatInvitationCode.objects.filter(invitation_code=invitation_code).first()
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
                        models.CodeToken.objects.update_or_create(defaults={'token': token, 'token_effective_time': effective_time}, code=invitation_code_object)
                    #     return manufactor_id and edition_id string
                    #     manufactor = request.user.Retail.Product.filter()
                    #     edition_objects = models.ZyjWechatEdition.objects.filter(Manufactor=manufactor_id)
                    else:
                        responses['code'] = 2001
                        responses['message'] = "邀请码过期，请填写可用的邀请码"
                else:
                    models.CodeToken.objects.update_or_create(code=invitation_code_object, defaults={'token': token, 'token_effective_time': effective_time})
                    responses['token'] = token
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
                # 建立链接,服务器为客户端，硬件为服务端
            address_ip = equipment_obj.ip
            address_port = equipment_obj.port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # l_onoff = 1
            # l_linger = 0
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', l_onoff, l_linger))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ip_port = ('0.0.0.0', 3367)
            sock.connect(ip_port)
            send_data_dict = {
                    "address_ip": address_ip,
                    "address_port": address_port,
                    "value": value,
                    "number": equipment_number
                }
            send_data_str = json.dumps(send_data_dict)
            data = bytes(send_data_str, 'utf-8')
            sock.send(data)
            sock.close()
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
            if methanal_obj:
                methanal_time_list = methanal_obj.time.split(',')
                methanal_value_str = methanal_obj.methanal_value
                methanal_time_list.pop()
                value_CO2_list = []
                value_methanal_list = []
                methanal_value_list = methanal_value_str.split(';')
                methanal_value_list.pop()
                for methanal_value in methanal_value_list:
                    methanal_value_dict = json.loads(methanal_value)
                    value_CO2 = methanal_value_dict['CO2']
                    value_methanal = methanal_value_dict['methanal']
                    value_CO2_list.append(value_CO2)
                    value_methanal_list.append(value_methanal)
                methanal_dict = {
                    "methanal_time": methanal_time_list,
                    "methanal_value": value_methanal_list,
                    "CO2_value": value_CO2_list
                }
                responses['data'] = methanal_dict
            else:
                responses['code'] = 3003
                responses['message'] = "该验证码无可用设备"
                responses['data'] = []
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
            banners_obj = models.Banner.objects.filter(location=location).all()
            if banners_obj:
                for banner_obj in banners_obj:
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