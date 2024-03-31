from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Image
import os
from django.conf import settings

@receiver(post_delete, sender=Image)
def delete_associated_image(sender, instance, **kwargs):
    """Image 모델 인스턴스가 삭제될 때 연관된 이미지 파일도 삭제"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
