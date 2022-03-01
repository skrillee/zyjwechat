__author__ = 'Yan.zhe 2021.09.28'

from django.conf.urls import url
from wechat import views

urlpatterns = [
    url(r'^v1/auth/$', views.AuthVIew.as_view()),
    url(r'^v1/retail/$', views.RetailVIew.as_view()),
    url(r'^v1/manufactor/$', views.Manufactor.as_view()),
    url(r'^v1/manufactor_picture/(\w+\.(?:png|jpg|gif|bmp))/$', views.ManufactorPicture.as_view()),
    url(r'^v1/edition/(\w+)/$', views.Edition.as_view()),
    url(r'^v1/model/$', views.Model.as_view()),
    url(r'^v1/model/sample/$', views.Sample.as_view()),
    url(r'^v1/retail/artificial/$', views.Artificial.as_view()),
    url(r'^v1/retail/ingredients/$', views.Ingredients.as_view()),
    url(r'^v1/retail/classification/$', views.Classification.as_view()),
    url(r'^v1/retail/voucher/$', views.Voucher.as_view()),
    url(r'^v1/retail/mqtt/$', views.Methanal.as_view()),
    url(r'^v1/retail/methanal_result/$', views.Result.as_view()),
    url(r'^v1/retail/banners/$', views.Banner.as_view()),
    url(r'^v1/retail/history/$', views.History.as_view()),
    # url(r'^v1/retail/callback/$', views.Callback.as_view()),
    url(r'^v1/retail/pay/$', views.Login.as_view()),
    url(r'^v1/retail/live/$', views.Live.as_view()),
    url(r'^v1/retail/room/$', views.Room.as_view()),
    url(r'^v1/retail/status/$', views.Status.as_view()),
    url(r'^v1/retail/ticket/$', views.Ticket.as_view()),
    url(r'^v1/retail/bill_detail/$', views.BillDetail.as_view()),
    # url(r'^v1/retail/pay/$', views.Login.as_view()),
]
