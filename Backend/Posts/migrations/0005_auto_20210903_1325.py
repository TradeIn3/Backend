# Generated by Django 3.2.6 on 2021-09-03 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_alter_profile_user_id'),
        ('Posts', '0004_remove_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Profile.profile'),
        ),
        migrations.CreateModel(
            name='SavedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Posts.post')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Profile.profile')),
            ],
        ),
    ]