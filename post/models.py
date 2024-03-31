from django.db import models
from django.conf import settings
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.pk})


class Text(models.Model):
    post = models.ForeignKey(Post, related_name='texts', on_delete=models.CASCADE)
    content = models.TextField()

class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_img/')
