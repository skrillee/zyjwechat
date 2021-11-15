# Generated by Django 3.0.8 on 2021-11-15 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0005_auto_20211106_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZyjWechatIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True, unique=True, verbose_name='辅料名称')),
                ('product_name', models.CharField(max_length=128, null=True, verbose_name='品牌名称')),
                ('images', models.CharField(max_length=1024, null=True, verbose_name='图片')),
                ('specification', models.CharField(max_length=128, null=True, verbose_name='规格')),
                ('reference_price', models.FloatField(max_length=64, null=True, verbose_name='参考价格')),
                ('area_size', models.CharField(max_length=1024, null=True, verbose_name='可用面积')),
                ('explain', models.CharField(max_length=1024, null=True, verbose_name='使用说明')),
                ('Retail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat.ZyjWechatRetail')),
            ],
            options={
                'verbose_name': '辅料',
                'verbose_name_plural': '辅料集合',
            },
        ),
        migrations.CreateModel(
            name='ZyjWechatArtificial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='施工组名称')),
                ('number', models.CharField(max_length=64, verbose_name='人数')),
                ('reference_price', models.FloatField(max_length=64, verbose_name='参考价格')),
                ('experience', models.CharField(max_length=64, verbose_name='工作经验')),
                ('Retail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat.ZyjWechatRetail')),
            ],
            options={
                'verbose_name': '施工',
                'verbose_name_plural': '施工集合',
            },
        ),
    ]
