import pytz
import datetime
from wechat import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_object = models.CodeToken.objects.filter(token=token).first()
        if not token_object:
            raise exceptions.AuthenticationFailed('认证失败，请填写邀请码后查看')
        else:
            token_effective_time = token_object.token_effective_time
            current_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            remaining_time = current_time - token_object.first_loading
            time_state = remaining_time < datetime.timedelta(days=token_effective_time)
            if time_state:
                return token_object.code, token_object
            else:
                raise exceptions.AuthenticationFailed('邀请码过期，请填写可用的邀请码')

    def authenticate_header(self, request):
        """
        when Authentication failed：
            Return a string to be used as the value of the `WWW-Authenticate`
            header in a `401 Unauthenticated` response, or `None` if the
            authentication scheme should return `403 Permission Denied` responses.
        """
        pass


# noinspection PyProtectedMember,PyMethodMayBeStatic,PyBroadException,PyUnresolvedReferences
class AuthenticationOverdue(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_object = models.CodeToken.objects.filter(token=token, is_valid=True).first()
        if not token_object:
            raise exceptions.AuthenticationFailed('认证失败，请填写邀请码后查看')
        return token_object.code, token_object

    def authenticate_header(self, request):
        """
        when Authentication failed：
            Return a string to be used as the value of the `WWW-Authenticate`
            header in a `401 Unauthenticated` response, or `None` if the
            authentication scheme should return `403 Permission Denied` responses.
        """
        pass
