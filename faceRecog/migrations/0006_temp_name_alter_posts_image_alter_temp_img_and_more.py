# Generated by Django 4.0.4 on 2022-05-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecog', '0005_temp_userface'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='name',
            field=models.CharField(default='-', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(default='images/user.jpeg', upload_to='posts/'),
        ),
        migrations.AlterField(
            model_name='temp',
            name='img',
            field=models.ImageField(default='images/user.jpeg', upload_to='dp/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='images/user.jpeg', upload_to='dp/'),
        ),
        migrations.AlterField(
            model_name='userface',
            name='registered_face',
            field=models.ImageField(default='images/user.jpeg', upload_to='faces/'),
        ),
    ]
