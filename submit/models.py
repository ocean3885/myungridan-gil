from django.db import models
from django.conf import settings


class Submit(models.Model):

    class Meta:
        ordering = ['-created']

    CATEGORY_CHOICES = [
        ("jm", "신생아작명"),
        ("gm", "개명신청"),
        ("sj", "사주상담"),
        ("etc", "기타"),
    ]

    PROCESS_CHOICES = [
        ("1", "입금대기"),
        ("2", "진행중"),
        ("3", "완료"),
    ]

    VISIT_CHOICES = [
        ("visit", "방문상담"),
        ("call", "전화상담"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visit = models.CharField(max_length=20, choices=VISIT_CHOICES, blank=True)
    wantdate = models.CharField(max_length=30, blank=True)
    dad_name = models.CharField(max_length=25, blank=True)
    mom_name = models.CharField(max_length=25, blank=True)
    first_name_ch = models.CharField(max_length=25, blank=True)
    first_name_kr = models.CharField(max_length=25, blank=True)
    first_name_bon = models.CharField(max_length=25, blank=True)
    dolrim = models.CharField(max_length=25, blank=True)
    fav_name = models.CharField(max_length=100, blank=True)
    avoid_name = models.CharField(max_length=100, blank=True)
    adress = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, max_length=254)
    description = models.TextField(blank=True)
    process = models.CharField(max_length=20, choices=PROCESS_CHOICES, blank=True, default="1")

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=50, blank=True)
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='persons')
    gen = models.CharField(max_length=1)
    sl = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    hour = models.CharField(max_length=2)
    min = models.CharField(max_length=2)

    def __str__(self):
        return self.name