# Generated by Django 3.2.9 on 2022-02-23 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0023_zyjwechatinvitationcode_liveroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zyjwechatinvitationcode',
            name='LiveRoom',
        ),
    ]
