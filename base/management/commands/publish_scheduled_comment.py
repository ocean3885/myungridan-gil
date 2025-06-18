from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError, DatabaseError
from django.contrib.auth.models import User
from base.models import ScheduledItem, CustomComment
import logging
import traceback


logger = logging.getLogger(__name__) # 모듈 레벨 로거
class Command(BaseCommand):
    help = "글이 발행된 아이템의 예약 댓글을 발행합니다."

    def handle(self, *args, **options):
        # 글은 발행되었으나 댓글은 아직인 아이템들을 찾습니다.
        items_to_process = ScheduledItem.objects.filter(
            status=ScheduledItem.Status.POST_PUBLISHED
        )

        # 운영자 계정을 미리 가져옵니다.
        try:
            admin_user = User.objects.get(pk=1)
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    "운영자 계정(pk=1)을 찾을 수 없습니다. 댓글을 발행할 수 없습니다."
                )
            )
            return

        for item in items_to_process:
            if not item.published_board or not item.comment_content:
                self.stderr.write(self.style.ERROR(f"아이템 {item.id}에 필수 값이 누락되었습니다."))
                continue
            try:
                with transaction.atomic():
                    
                    # 실제 CustomComment 객체 생성 (작성자는 admin_user로 고정)
                    new_comment = CustomComment.objects.create(
                        board=item.published_board,
                        user=admin_user,
                        content=item.comment_content,
                    )

                    # 아이템의 상태를 '전체 발행 완료'로 변경
                    # item.status = ScheduledItem.Status.ALL_PUBLISHED
                    # item.published_comment = new_comment  # 생성된 댓글과 연결
                    # item.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'성공적으로 댓글을 발행했습니다: on post "{item.post_title}"'
                    )
                )

            except IntegrityError as e:
                self.stderr.write(self.style.ERROR(f"무결성 오류 발생 on item {item.id}: {e}"))
                logger.exception(f"무결성 오류 발생 on item {item.id}")
            except DatabaseError as e:
                self.stderr.write(self.style.ERROR(f"데이터베이스 오류 발생 on item {item.id}: {e}"))
                logger.exception(f"데이터베이스 오류 발생 on item {item.id}")
            except Exception as e:
                item.status = ScheduledItem.Status.ERROR
                item.save()
                error_traceback = traceback.format_exc()
                self.stderr.write(self.style.ERROR(f"댓글 발행 중 오류 발생 on item {item.id}: {e}\n{error_traceback}"))
                logger.exception(f"댓글 발행 중 오류 발생 on item {item.id}")