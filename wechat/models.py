__author__ = 'Yan.zhe 2021.09.28'

from django.db import models


class ZyjWechatRetail(models.Model):
    shop_name = models.CharField('店铺名称', unique=True, max_length=128)
    master_name = models.CharField('负责人名称', max_length=128)
    phone = models.CharField('客服手机号码', max_length=32)
    qq_number = models.CharField('客服qq号码', max_length=32)
    wechat_number = models.CharField('客服微信号码', max_length=64)
    address = models.CharField('店铺地址', max_length=128)
    email = models.CharField('邮箱', max_length=128)
    shop_introduction = models.CharField('店铺简介', max_length=256)
    Product = models.ManyToManyField('ZyjWechatManufactor')

    class Meta:
        verbose_name = '零售商'
        verbose_name_plural = '零售商集合'


class ZyjWechatInvitationCode(models.Model):
    code_type_choice = (
        (1, '一级邀请码'),
        (2, '二级邀请码'),
        (3, '三级邀请码'),
    )
    code_type = models.IntegerField(choices=code_type_choice)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    invitation_code = models.CharField('邀请码', unique=True, max_length=64)
    effective_time = models.IntegerField('有效时间', default=3)

    class Meta:
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码集合'


class CodeToken(models.Model):
    code = models.OneToOneField(to=ZyjWechatInvitationCode, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    first_loading = models.DateTimeField('首次登陆时间', auto_now_add=True)
    token_effective_time = models.IntegerField('有效时间', default=3)

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'token'


class ZyjWechatManufactor(models.Model):
    name = models.CharField('生产商名称', unique=True, max_length=128)
    manufactor_introduction = models.CharField('生产商简介', max_length=256)
    manufactor_logo = models.CharField('商标', max_length=512)
    manufactor_sample = models.CharField('宣传图', max_length=1024)

    class Meta:
        verbose_name = '生产商'
        verbose_name_plural = '生产商集合'


class ZyjWechatArtificial(models.Model):
    name = models.CharField('施工组名称', unique=True, max_length=128)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    number = models.CharField('人数', max_length=64)
    reference_price = models.FloatField('参考价格', max_length=64)
    experience = models.CharField('工作经验', max_length=64)

    class Meta:
        verbose_name = '施工'
        verbose_name_plural = '施工集合'


class ZyjWechatEdition(models.Model):
    name = models.CharField('版本名称', unique=True, max_length=128)
    Manufactor = models.ForeignKey(ZyjWechatManufactor, on_delete=models.CASCADE, null=True)
    style = models.CharField('版本风格', max_length=128)
    date = models.CharField('版本上线日期', max_length=128)
    edition_sample = models.CharField('宣传图', max_length=1024)

    class Meta:
        verbose_name = '版本'
        verbose_name_plural = '版本集合'


class ZyjWechatModel(models.Model):
    name = models.CharField('型号名称', unique=True, max_length=128)
    Edition = models.ForeignKey(ZyjWechatEdition, on_delete=models.CASCADE, null=True)
    scene = models.CharField('场景', max_length=128)
    date = models.CharField('上线日期', max_length=128)
    model_sample = models.CharField('宣传图', max_length=1024)
    model_unit = models.CharField('单元图', max_length=1024)
    VR_address = models.CharField('实景图链接', max_length=1024)
    reference_price = models.FloatField('参考价格', max_length=64)
    size = models.CharField('规格尺寸', max_length=64)
    details = models.CharField('详情介绍', max_length=1024)
    VR_QR = models.CharField('实景图二维码', max_length=1024, null=True)

    class Meta:
        verbose_name = '型号'
        verbose_name_plural = '型号集合'


class ZyjWechatIngredients (models.Model):
    name = models.CharField('辅料名称', unique=True, max_length=128, null=True)
    product_name = models.CharField('品牌名称', max_length=128, null=True)
    images = models.CharField('图片', max_length=1024, null=True)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    specification = models.CharField('规格', max_length=128, null=True)
    reference_price = models.FloatField('参考价格', max_length=64, null=True)
    area_size = models.CharField('可用面积', max_length=1024, null=True)
    explain = models.CharField('使用说明', max_length=1024, null=True)

    class Meta:
        verbose_name = '辅料'
        verbose_name_plural = '辅料集合'