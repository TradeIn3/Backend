# Generated by Django 3.2.6 on 2021-09-04 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0007_auto_20210903_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
