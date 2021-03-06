# Generated by Django 3.0.8 on 2021-11-23 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0008_classification_original_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='manual_price',
            field=models.FloatField(max_length=64, null=True, verbose_name='参考价格-包贴'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='original_price',
            field=models.FloatField(max_length=64, null=True, verbose_name='原价'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='reference_price',
            field=models.FloatField(max_length=64, null=True, verbose_name='参考价格-不包贴'),
        ),
    ]
