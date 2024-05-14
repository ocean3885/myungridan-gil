from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bgimg = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='default_bg.jpg')
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='default_user.png')
    image_thumb = ImageSpecField(source='picture',processors=[ResizeToFill(100, 100)],format='JPEG',options={'quality': 60})
    data = models.JSONField(default=dict,blank=True)
    gen = models.CharField(max_length=1,blank=True)
    sl = models.CharField(max_length=10,blank=True)
    year = models.CharField(max_length=4,blank=True)
    month = models.CharField(max_length=2,blank=True)
    day = models.CharField(max_length=2,blank=True)
    hour = models.CharField(max_length=2,blank=True)
    min = models.CharField(max_length=2,blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class CustomBoard(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CustomComment(models.Model):
    board = models.ForeignKey(CustomBoard, on_delete=models.CASCADE, related_name='board_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user}'