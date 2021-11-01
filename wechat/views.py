__author__ = 'Yan.zhe 2021.09.28'

from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse
from zyjwechat import settings
from wechat import models
import datetime
import hashlib
import time
import pytz
import os


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
            for single_manufactor in manufactor:
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
                }
                manufactor_message[single_manufactor.name] = single_manufactor_message
            responses['data'] = manufactor_message
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

