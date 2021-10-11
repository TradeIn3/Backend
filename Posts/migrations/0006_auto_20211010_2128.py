# Generated by Django 3.2.6 on 2021-10-10 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0005_order_reserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='year',
        ),
        migrations.AddField(
            model_name='post',
            name='brand',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='condition',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='reserved',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 9, 21, 28, 48, 542855)),
        ),
    ]