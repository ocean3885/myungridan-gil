from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post
import os

@receiver(post_delete, sender=Post)
def delete_attached_image(sender, instance, **kwargs):
    """
    Post 모델 인스턴스가 삭제될 때 첨부된 이미지 파일도 함께 삭제한다.
    """
    if instance.image:  # 'image'는 Post 모델의 이미지 필드 이름
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)