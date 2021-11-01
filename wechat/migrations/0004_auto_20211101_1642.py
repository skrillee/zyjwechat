# Generated by Django 3.0.8 on 2021-11-01 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_rename_manufactor_sample_zyjwechatedition_edition_sample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codetoken',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zyjwechatedition',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zyjwechatinvitationcode',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zyjwechatmanufactor',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zyjwechatretail',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='ZyjWechatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='型号名称')),
                ('scene', models.CharField(max_length=128, verbose_name='场景')),
                ('date', models.CharField(max_length=128, verbose_name='上线日期')),
                ('model_sample', models.CharField(max_length=1024, verbose_name='宣传图')),
                ('model_unit', models.CharField(max_length=1024, verbose_name='单元图')),
                ('VR_address', models.CharField(max_length=1024, verbose_name='实景图链接')),
                ('reference_price', models.FloatField(max_length=64, verbose_name='参考价格')),
                ('size', models.CharField(max_length=64, verbose_name='规格尺寸')),
                ('details', models.CharField(max_length=1024, verbose_name='详情介绍')),
                ('Edition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat.ZyjWechatEdition')),
            ],
            options={
                'verbose_name': '版本',
                'verbose_name_plural': '版本集合',
            },
        ),
    ]
