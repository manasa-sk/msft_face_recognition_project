# Generated by Django 4.0.4 on 2022-05-25 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('phone', models.PositiveBigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
