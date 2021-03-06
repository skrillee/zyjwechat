__author__ = 'Yan.zhe 2021.09.28'

from django.conf.urls import url
from wechat import views
from django.views.generic import RedirectView
app_name = 'wechat'

urlpatterns = [
    url(r'^v1/auth/$', views.AuthVIew.as_view()),
    url(r'^v1/mobile_phone/$', views.MobilePhone.as_view()),
    url(r'^v1/retail/$', views.RetailVIew.as_view()),
    url(r'^v1/manufactor/$', views.Manufactor.as_view()),
    url(r'^v1/manufactor_picture/(\w+\.(?:png|jpg|gif|bmp))/$', views.ManufactorPicture.as_view()),
    url(r'^v1/edition/(\w+)/$', views.Edition.as_view()),
    url(r'^v1/model/$', views.Model.as_view()),
    url(r'^v1/model/sample/$', views.Sample.as_view()),
    url(r'^v1/retail/artificial/$', views.Artificial.as_view()),
    url(r'^v1/retail/ingredients/$', views.Ingredients.as_view()),
    url(r'^v1/retail/classification/$', views.Classification.as_view()),
    url(r'^v1/retail/classification2/$', views.Classification2.as_view()),
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
    url(r'^v1/retail/bill/$', views.Bill.as_view()),
    url(r'^v1/retail/bill_detail/$', views.BillDetail.as_view()),
    url(r'^v1/retail/add_bill_detail/$', views.AddBillDetail.as_view()),
    url(r'^v1/retail/del_bill_detail/$', views.DelBillDetail.as_view()),
    url(r'^v1/retail/add_bill/$', views.AddBill.as_view()),
    url(r'^v1/retail/add_picture/$', views.AddPicture.as_view()),
    url(r'^v1/retail/check_picture/$', views.CheckPicture.as_view()),
    url(r'^v1/retail/contacts/$', views.Contacts.as_view()),
    url(r'^v1/retail/search_contacts/$', views.SearchContacts.as_view()),
    url(r'^v1/retail/add_order/$', views.AddOrder.as_view()),
    url(r'^v1/retail/delete_order/$', views.DeleteOrder.as_view()),
    url(r'^v1/retail/get_order/$', views.GetOrder.as_view()),
    url(r'^v1/retail/create_order/$', views.CreateOrder.as_view()),
    url(r'^v1/retail/video/$', views.GetVideo.as_view()),
    url(r'^v1/retail/redirect/$', views.Redirect.as_view()),
    url(r'^register/', views.douyin, name='douyin'),
    # url(r'^v1/retail/douyin/$', views.Douyin.as_view()),
    # url(r'^v1/retail/douyin/$', RedirectView.as_view(url='https://v.douyin.com/YPX29cs/'), name='douyin'),

    # url(r'^v1/retail/create_order/$', views.CreateOrder.as_view()),
    # url(r'^v1/retail/pay/$', views.Login.as_view()),
]
