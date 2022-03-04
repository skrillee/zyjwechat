# Generated by Django 3.2.9 on 2022-03-04 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0036_zyjwechatinvitationcode_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='zyjwechatinvitationcode',
            name='mobile',
            field=models.CharField(max_length=64, null=True, verbose_name='联系方式'),
        ),
        migrations.AddField(
            model_name='zyjwechatinvitationcode',
            name='street',
            field=models.CharField(max_length=128, null=True, verbose_name='地址'),
        ),
    ]
