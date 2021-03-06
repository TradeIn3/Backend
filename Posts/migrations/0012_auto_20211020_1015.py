# Generated by Django 3.2.6 on 2021-10-20 04:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_alter_profile_image'),
        ('Posts', '0011_auto_20211013_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.profile'),
        ),
        migrations.AlterField(
            model_name='reserved',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 10, 15, 1, 283027)),
        ),
    ]
