# Generated by Django 4.0.3 on 2022-05-29 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecog', '0011_user_about_alter_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faceRecog.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faceRecog.user')),
            ],
            options={
                'unique_together': {('user', 'post_id')},
            },
        ),
    ]