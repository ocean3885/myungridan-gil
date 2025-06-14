from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from base.models import ScheduledItem, CustomBoard

class Command(BaseCommand):
    help = '대기 중인 예약 아이템의 게시글 부분을 발행합니다.'

    def handle(self, *args, **options):
        item_to_publish = ScheduledItem.objects.filter(status=ScheduledItem.Status.PENDING).order_by('id').first()

        if not item_to_publish:
            self.stdout.write(self.style.SUCCESS('발행할 대기 중인 게시글이 없습니다.'))
            return

        try:
            with transaction.atomic():
                new_board = CustomBoard.objects.create(
                    name=item_to_publish.post_name,
                    title=item_to_publish.post_title,
                    content=item_to_publish.post_content,
                    password=item_to_publish.post_password,
                    is_secret=item_to_publish.post_is_secret
                )

                item_to_publish.status = ScheduledItem.Status.POST_PUBLISHED
                item_to_publish.post_published_at = timezone.now()
                item_to_publish.published_board = new_board
                item_to_publish.save()

            self.stdout.write(self.style.SUCCESS(f'성공적으로 포스트를 발행했습니다: "{new_board.title}"'))
        
        except Exception as e:
            if item_to_publish:
                item_to_publish.status = ScheduledItem.Status.ERROR
                item_to_publish.save()
            self.stderr.write(self.style.ERROR(f'포스트 발행 중 오류 발생: {e}'))