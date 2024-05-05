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

