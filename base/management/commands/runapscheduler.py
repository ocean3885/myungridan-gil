from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
import logging

logger = logging.getLogger(__name__)

def publish_post_job():
    """게시글 발행 커맨드를 호출하는 함수"""
    try:
        call_command('publish_scheduled_post')
    except Exception as e:
        # 오류 로그 등을 남길 수 있습니다.
        print(f"Error in publish_post_job: {e}")

def publish_comment_job():
    """댓글 발행 커맨드를 호출하는 함수"""
    try:
        call_command('publish_scheduled_comment')
    except Exception as e:
        print(f"Error in publish_comment_job: {e}")

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 1. 게시글 발행 작업: 매일 1회 실행
        scheduler.add_job(
            publish_post_job,
            'interval',
            hours=100,  # 36시간 간격으로 실행
            id='publish_post_job',   
            replace_existing=True,
        )
        
        # 2. 댓글 발행 작업: 매일 1회 실행
        scheduler.add_job(
            publish_comment_job,
            'cron',
            hour=9, 
            minute=5,  # 매일 오전 9시 5분에 실행
            id='publish_comment_job',     
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
