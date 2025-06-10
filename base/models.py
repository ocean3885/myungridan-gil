from django.conf import settings
import os
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bgimg = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
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
        # 1. User가 생성되면 일단 Profile을 먼저 생성합니다.
        profile = Profile.objects.create(user=instance)
        # 2. 기본 이미지 파일 경로를 설정합니다.
        default_pic_path = os.path.join(settings.BASE_DIR, 'static', 'base', 'img', 'default_user.png')
        default_bg_path = os.path.join(settings.BASE_DIR, 'static', 'base', 'img', 'default_bg.jpg')

        # 3. 기본 프로필 이미지가 존재하는지 확인하고, 파일을 열어서 Profile에 할당합니다.
        if os.path.exists(default_pic_path):
            with open(default_pic_path, 'rb') as f:
                profile.picture.save('default_user.png', File(f), save=False)

        # 4. 기본 배경 이미지가 존재하는지 확인하고, 파일을 열어서 Profile에 할당합니다.
        if os.path.exists(default_bg_path):
            with open(default_bg_path, 'rb') as f:
                profile.bgimg.save('default_bg.jpg', File(f), save=False)
        
        # 5. 모든 이미지 할당이 끝난 후, 마지막에 한 번만 profile 전체를 저장합니다.
        profile.save()
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class CustomBoard(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_secret = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class CustomComment(models.Model):
    board = models.ForeignKey(CustomBoard, on_delete=models.CASCADE, related_name='board_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password = models.CharField(max_length=20,blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user}'
    
    
class ScheduledItem(models.Model):
    """자동 등록될 (게시글 + 댓글) 묶음 저장 모델"""
    class Status(models.TextChoices):
        PENDING = 'PENDING', '발행 대기'
        POST_PUBLISHED = 'POST_PUBLISHED', '글 발행 완료'
        ALL_PUBLISHED = 'ALL_PUBLISHED', '전체 발행 완료'
        ERROR = 'ERROR', '오류'

    # --- 게시글 정보 ---
    post_name = models.CharField(max_length=10, verbose_name="작성자 이름")
    post_title = models.CharField(max_length=200, verbose_name="게시글 제목")
    post_is_secret = models.BooleanField(default=False, verbose_name="비공개 여부")
    post_password = models.CharField(max_length=20, default="0632857255", verbose_name="게시글 비밀번호")
    post_content = models.TextField(verbose_name="게시글 내용")

    # --- 댓글 정보 ---
    comment_content = models.TextField(verbose_name="댓글 내용")
    comment_publish_delay_minutes = models.PositiveIntegerField(
        default=60, 
        verbose_name="댓글 발행 지연(분)",
        help_text="게시글이 발행된 후 몇 분 뒤에 댓글을 등록할지 설정합니다."
    )

    # --- 발행 상태 및 추적 정보 ---
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    post_published_at = models.DateTimeField(null=True, blank=True, verbose_name="글 발행 시각")
    
    # 생성된 실제 객체들과 연결 (추적 및 관리 용이)
    published_board = models.OneToOneField(CustomBoard, on_delete=models.SET_NULL, null=True, blank=True)
    published_comment = models.OneToOneField(CustomComment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = "예약 발행 아이템"
        verbose_name_plural = "예약 발행 아이템 목록"

    def __str__(self):
        return f'[예약] {self.post_title}'