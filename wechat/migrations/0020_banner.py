# Generated by Django 3.0.8 on 2021-12-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0019_auto_20211208_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128, null=True, verbose_name='位置')),
                ('images', models.CharField(max_length=1024, null=True, verbose_name='图片')),
                ('describe', models.CharField(max_length=128, null=True, verbose_name='描述')),
                ('category', models.CharField(max_length=128, null=True, verbose_name='品类')),
                ('remark', models.CharField(max_length=128, null=True, verbose_name='备注')),
            ],
        ),
    ]