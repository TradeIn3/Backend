# Generated by Django 3.2.6 on 2021-09-04 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0009_postimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='time',
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
