# Generated by Django 3.2.6 on 2021-09-01 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_id',
            field=models.CharField(max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]