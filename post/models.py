from django.db import models
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_img/')
    created_at = models.DateTimeField(auto_now_add=True)  # 포스트가 생성될 때의 날짜/시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.pk})


