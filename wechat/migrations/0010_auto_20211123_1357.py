# Generated by Django 3.0.8 on 2021-11-23 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0009_auto_20211123_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='details',
            field=models.CharField(max_length=1024, null=True, verbose_name='详情介绍'),
        ),
        migrations.AddField(
            model_name='classification',
            name='evaluate',
            field=models.CharField(max_length=64, null=True, verbose_name='30平米包工包料价格'),
        ),
        migrations.AddField(
            model_name='classification',
            name='size',
            field=models.CharField(max_length=64, null=True, verbose_name='规格尺寸'),
        ),
    ]
