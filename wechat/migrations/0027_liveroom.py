# Generated by Django 3.2.9 on 2022-02-23 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0026_delete_liveroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anchor_name', models.CharField(max_length=64, null=True, verbose_name='主播名称')),
                ('anchor_wechat', models.CharField(max_length=64, null=True, verbose_name='主播微信')),
                ('media_id', models.CharField(max_length=128, null=True, verbose_name='媒体标识')),
                ('room_belong', models.CharField(max_length=128, null=True, verbose_name='直播间所属')),
                ('room_id', models.CharField(max_length=32, null=True, verbose_name='直播间id')),
                ('room_name', models.CharField(max_length=64, null=True, verbose_name='直播间名称')),
            ],
            options={
                'verbose_name': '直播间',
                'verbose_name_plural': '直播间集合',
            },
        ),
    ]
