# Generated by Django 3.0.8 on 2021-11-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0010_auto_20211123_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='discount',
            field=models.FloatField(max_length=32, null=True, verbose_name='折扣商品'),
        ),
    ]
