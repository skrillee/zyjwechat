# Generated by Django 3.0.8 on 2021-11-23 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0007_classification_voucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='original_price',
            field=models.FloatField(max_length=64, null=True, verbose_name='原价价格'),
        ),
    ]