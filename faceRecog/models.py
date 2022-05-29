from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    profile_pic = models.ImageField(upload_to='dp/', default='images/user.jpeg')
    password = models.CharField(max_length=30)

    is_active = models.BooleanField(default=False)
    about = models.TextField(max_length=200, default='-')

    def __str__(self):
        return self.username


class Posts(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', default='images/user.jpeg')
    post_id = models.AutoField(primary_key=True, auto_created=True, serialize=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0, null=False)

class LikedBy(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('user', 'post_id'),)

class PostPeople(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    class Meta:
        unique_together = (('username', 'post_id'),)
