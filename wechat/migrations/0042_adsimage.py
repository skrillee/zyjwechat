# Generated by Django 3.2.9 on 2023-08-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0041_totalcolor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ads_image_id', models.CharField(max_length=64, null=True, verbose_name='id')),
                ('ads_image_type', models.CharField(max_length=64, null=True, verbose_name='类型')),
                ('ads_image_page', models.CharField(max_length=64, null=True, verbose_name='页面')),
                ('ads_image_name', models.CharField(max_length=64, null=True, verbose_name='位置')),
                ('ads_image_title', models.CharField(max_length=64, null=True, verbose_name='标题')),
                ('ads_image_status', models.CharField(max_length=64, null=True, verbose_name='状态')),
                ('ads_image_pic', models.CharField(max_length=128, null=True, verbose_name='图片')),
                ('ads_image_size', models.CharField(max_length=128, null=True, verbose_name='图片尺寸')),
                ('ads_image_remark', models.CharField(max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '广告图片信息',
                'verbose_name_plural': '广告图片信息',
            },
        ),
    ]
