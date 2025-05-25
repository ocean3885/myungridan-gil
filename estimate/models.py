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
    name = models.CharField(max_length=50, blank=True)
    name_hanja = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, max_length=254)
    description = models.TextField(blank=True)
    process = models.CharField(max_length=20, choices=PROCESS_CHOICES, blank=True, default="1")
    data = models.JSONField(default=dict)
    gen = models.CharField(max_length=10)
    sl = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    hour = models.CharField(max_length=2)
    min = models.CharField(max_length=2)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_public = models.BooleanField(default=True)

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
    
    
class InmyungHanja(models.Model):
    num = models.IntegerField("번호")  
    pron = models.CharField("발음", max_length=10)
    char = models.CharField("한자", max_length=10)
    main_mean = models.CharField("뜻", max_length=100)
    tot_stk = models.IntegerField("전체획수")
    main_elem = models.CharField("한자오행", max_length=10)
    disused = models.BooleanField("불용한자", default=False)
    rad_stk = models.IntegerField("부수획수")
    rad = models.CharField("부수한자", max_length=10)
    rad_elem = models.CharField("부수오행", max_length=10)
    detail_mean = models.TextField("세부뜻")
    meaning = models.CharField("의미발음", max_length=100)
    stk_info = models.CharField("획수정보", max_length=50)
    rad_id = models.IntegerField("부수번호")
    no_rad_stk = models.IntegerField("부수제외획수")
    rad_mean = models.CharField("부수뜻", max_length=100)

    def __str__(self):
        return f"{self.char} ({self.pron}) - {self.main_mean}"