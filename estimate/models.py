from django.db import models
from django.conf import settings


class Estimate(models.Model):

    class Meta:
        ordering = ['-created']


    PROCESS_CHOICES = [
        ("1", "대기중"),
        ("2", "감명완료"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, max_length=254)
    description = models.TextField(blank=True)
    process = models.CharField(max_length=20, choices=PROCESS_CHOICES, blank=True, default="1")
    data = models.JSONField(default=dict)
    gen = models.CharField(max_length=1)
    sl = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    hour = models.CharField(max_length=2)
    min = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user}'