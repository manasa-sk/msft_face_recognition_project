# Generated by Django 4.0.3 on 2022-05-28 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecog', '0010_remove_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
