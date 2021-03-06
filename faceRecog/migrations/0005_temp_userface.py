# Generated by Django 4.0.4 on 2022-05-26 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecog', '0004_remove_user_f_name_remove_user_l_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('img', models.ImageField(default='black.jpeg', upload_to='dp')),
            ],
        ),
        migrations.CreateModel(
            name='Userface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_face', models.ImageField(default='user.jpeg', upload_to='faces')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
