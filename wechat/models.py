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
    advertiser = models.CharField('下游广告商', max_length=128, null=True)
    Product = models.ManyToManyField('ZyjWechatManufactor')

    class Meta:
        verbose_name = '零售商'
        verbose_name_plural = '零售商集合'


class LivingRoom(models.Model):
    anchor_name = models.CharField('主播名称', max_length=64, null=True)
    anchor_wechat = models.CharField('主播微信', max_length=64, null=True)
    media_id = models.CharField('媒体标识', max_length=128, null=True)
    room_belong = models.CharField('直播间所属', max_length=128, null=True)
    room_id = models.CharField('直播间id', max_length=32, null=True)
    room_name = models.CharField('直播间名称', max_length=64, null=True)

    class Meta:
        verbose_name = '直播间'
        verbose_name_plural = '直播间集合'


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
    # LiveRoom = models.IntegerField('有效时间', default=3)
    LiveRoom = models.ForeignKey(LivingRoom, on_delete=models.CASCADE, null=True)
    name = models.CharField('名字', null=True, max_length=64)
    mobile = models.CharField('联系方式', null=True, max_length=64)
    street = models.CharField('地址', null=True, max_length=128)

    class Meta:
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码集合'


class ZyjWechatBill(models.Model):
    customer_name = models.CharField('客户名称', max_length=128, null=True)
    cost_name = models.CharField('费用名称', max_length=128, null=True)
    unit_price = models.CharField('单价', max_length=128, null=True)
    quantity = models.CharField('数量', max_length=128, null=True)
    trading_time = models.CharField('交易时间', max_length=128, null=True)
    chart_color = models.CharField('图表颜色', max_length=128, null=True)
    InvitationCode = models.ForeignKey(ZyjWechatInvitationCode, on_delete=models.CASCADE, null=True)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    remark = models.CharField('备注', max_length=128, null=True)

    class Meta:
        verbose_name = '账单'
        verbose_name_plural = '账单集合'


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


class ZyjWechatIngredients(models.Model):
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


class Classification(models.Model):
    name = models.CharField('名称', unique=True, max_length=128, null=True)
    product_name = models.CharField('品牌名称', max_length=128, null=True)
    images_small = models.CharField('图片', max_length=1024, null=True)
    images_big = models.CharField('图片', max_length=1024, null=True)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    reference_price = models.FloatField('参考价格-不包贴', max_length=64, null=True)
    original_price = models.FloatField('原价', max_length=64, null=True)
    manual_price = models.FloatField('参考价格-包贴', max_length=64, null=True)
    characteristic = models.CharField('图案类型', max_length=64, null=True)
    discount = models.CharField('折扣商品', max_length=32, null=True)
    size = models.CharField('规格尺寸', max_length=64, null=True)
    details = models.CharField('详情介绍', max_length=1024, null=True)
    evaluate = models.CharField('30平米包工包料价格', max_length=64, null=True)
    images_parameter = models.CharField('图片', max_length=1024, null=True)

    class Meta:
        verbose_name = '种类'
        verbose_name_plural = '种类集合'


class Voucher(models.Model):
    name = models.CharField('名称', unique=True, max_length=128, null=True)
    phone = models.CharField('客服手机号码', max_length=32)
    address = models.CharField('店铺地址', max_length=128)
    reduction = models.CharField('满减', max_length=128, null=True)
    images_small = models.CharField('图片', max_length=1024, null=True)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)
    remaining = models.FloatField('剩余个数', max_length=64, null=True)
    state = models.FloatField('状态', max_length=64, null=True)
    verification = models.FloatField('验证码', max_length=64, null=True)

    class Meta:
        verbose_name = '满减券'
        verbose_name_plural = '满减券'


class Methanal(models.Model):
    number = models.CharField('设备编号', max_length=128, null=True)
    invitation_code = models.CharField('邀请码', max_length=128, null=True)
    methanal_value = models.CharField('甲醛含量', max_length=1024, null=True)
    ip = models.CharField('地址', max_length=128, null=True)
    port = models.CharField('端口', max_length=32, null=True)
    time = models.CharField('时间', max_length=32, null=True)

    class Meta:
        verbose_name = '甲醛检测'
        verbose_name_plural = '甲醛检测'


class Equipment(models.Model):
    ip = models.CharField('地址', max_length=128, null=True)
    port = models.CharField('端口', max_length=32, null=True)
    number = models.CharField('设备编号', max_length=128, null=True, unique=True)
    invitation_code = models.CharField('邀请码', max_length=128, null=True)
    status = models.CharField('状态', max_length=32, null=True)


class Banner(models.Model):
    location = models.CharField('位置', max_length=128, null=True)
    images = models.CharField('图片', max_length=1024, null=True)
    describe = models.CharField('描述', max_length=128, null=True)
    category = models.CharField('品类', max_length=128, null=True)
    remark = models.CharField('备注', max_length=128, null=True)


class Ticket(models.Model):
    ticket_name = models.CharField('券名', max_length=32, null=True)
    ticket_image = models.CharField('券缩略图', max_length=128, null=True)
    ticket_image_detail = models.CharField('券详情图', max_length=128, null=True)
    ticket_active = models.BooleanField('是否有效', max_length=128, null=True)
    ticket_type = models.CharField('券类型', max_length=32, null=True)
    ticket_information = models.CharField('券说明', max_length=1024, null=True)
    remark = models.CharField('备注', max_length=128, null=True)
    Retail = models.ForeignKey(ZyjWechatRetail, on_delete=models.CASCADE, null=True)


class Cart(models.Model):
    cart_create_time = models.DateTimeField('临时选中商品的时间', auto_now_add=True)
    Classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)
    cart_code = models.CharField('邀请码', max_length=32, null=True)

    class Meta:
        verbose_name = '临时选中的商品'
        verbose_name_plural = '临时选中的商品'


class Order(models.Model):
    order_create_time = models.DateTimeField('订单创建时间', auto_now_add=True)
    order_local = models.CharField('预约地点', max_length=64, null=True)
    order_owner = models.CharField('客户姓名', max_length=32, null=True)
    order_time = models.CharField('预约时间', max_length=32, null=True)
    order_phone = models.CharField('电话', max_length=32, null=True)
    order_code = models.CharField('邀请码', max_length=32, null=True)
    remark = models.CharField('备注', max_length=128, null=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'


class ColorType(models.Model):
    color_type_id = models.CharField('颜色类型名称', max_length=128, null=True)
    color_type_pic = models.CharField('单元图', max_length=128, null=True)
    remark = models.CharField('备注', max_length=128, null=True)

    class Meta:
        verbose_name = '颜色类型名称'
        verbose_name_plural = '颜色类型名称集合'


class ColorUnit(models.Model):
    color_id = models.CharField('色号编码', max_length=32, null=True)
    color_name = models.CharField('色号名称', max_length=128, null=True)
    color_type = models.CharField('色号类型', max_length=32, null=True)
    color_unit_pic = models.CharField('单元图', max_length=128, null=True)
    color_pic_1 = models.CharField('效果图1', max_length=128, null=True)
    color_pic_2 = models.CharField('效果图1', max_length=128, null=True)
    color_pic_3 = models.CharField('效果图1', max_length=128, null=True)
    color_pic_4 = models.CharField('效果图1', max_length=128, null=True)
    remark = models.CharField('备注', max_length=128, null=True)
    Retail = models.ForeignKey(ColorType, on_delete=models.CASCADE, null=True)


class TotalColor(models.Model):
    color_name = models.CharField('颜色简码', max_length=128, null=True)
    color_rgb = models.CharField('颜色RGB', max_length=128, null=True)
    hubuse_name = models.CharField('互补色简码', max_length=128, null=True)
    hubuse_rgb = models.CharField('互补色RGB', max_length=128, null=True)
    leibise_name = models.CharField('类比色简码', max_length=128, null=True)
    leibise_rgb = models.CharField('类比色RGB', max_length=128, null=True)
    jianbianse_name = models.CharField('类比色简码', max_length=128, null=True)
    jianbianse_rgb = models.CharField('类比色RGB', max_length=128, null=True)
    color_type = models.CharField('颜色类别', max_length=128, null=True)
    color_system = models.CharField('颜色色系', max_length=128, null=True)
    remark = models.CharField('备注', max_length=128, null=True)

    class Meta:
        verbose_name = '全色卡名称'
        verbose_name_plural = '全色卡名称集合'


class AdsImage(models.Model):
    ads_image_id = models.CharField('id', max_length=64, null=True)
    ads_image_type = models.CharField('类型', max_length=64, null=True)
    ads_image_page = models.CharField('页面', max_length=64, null=True)
    ads_image_name = models.CharField('位置', max_length=64, null=True)
    ads_image_title = models.CharField('标题', max_length=64, null=True)
    ads_image_status = models.CharField('状态', max_length=64, null=True)
    ads_image_pic = models.CharField('图片', max_length=128, null=True)
    ads_image_size = models.CharField('图片尺寸', max_length=128, null=True)
    ads_image_remark = models.CharField('备注', max_length=128, null=True)

    class Meta:
        verbose_name = '广告图片信息'
        verbose_name_plural = '广告图片信息'
