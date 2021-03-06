# Generated by Django 4.0.4 on 2022-05-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecog', '0008_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Temp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
