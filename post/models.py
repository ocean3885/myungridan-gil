from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    count = models.IntegerField(default=0)
    is_all = models.BooleanField(default=False)
    is_side = models.BooleanField(default=False)
    is_home = models.CharField(max_length=10, null=True, blank=True)  
    image = models.ImageField(upload_to='post_img/')
    image_thumb = ImageSpecField(source='image',processors=[ResizeToFill(100, 100)],format='JPEG',options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)  # 포스트가 생성될 때의 날짜/시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.pk})

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} likes {self.post}'
    
    
class DraftPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='draft_posts', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='draft_post_img/', blank=True, null=True) # Make image optional for drafts
    image_thumb = ImageSpecField(source='image',
                                 processors=[ResizeToFill(100, 100)],
                                 format='JPEG',
                                 options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Draft Post"
        verbose_name_plural = "Draft Posts"
