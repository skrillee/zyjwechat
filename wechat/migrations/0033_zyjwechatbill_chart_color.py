# Generated by Django 3.2.9 on 2022-02-27 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0032_zyjwechatbill'),
    ]

    operations = [
        migrations.AddField(
            model_name='zyjwechatbill',
            name='chart_color',
            field=models.CharField(max_length=128, null=True, verbose_name='图表颜色'),
        ),
    ]
