# Generated by Django 3.2.4 on 2021-10-19 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_auto_20211019_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zyjwechatedition',
            old_name='manufactor_sample',
            new_name='edition_sample',
        ),
    ]
