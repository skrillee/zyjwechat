# Generated by Django 3.2.9 on 2022-02-23 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0022_liveroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='zyjwechatinvitationcode',
            name='LiveRoom',
            field=models.IntegerField(default=3, verbose_name='有效时间'),
        ),
    ]