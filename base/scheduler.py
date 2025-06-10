from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django_apscheduler.jobstores import DjangoJobStore

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

def start():
    scheduler = BackgroundScheduler()
    # Django DB를 작업 저장소로 사용하여 스케줄링 정보를 영구적으로 관리
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 작업 등록
    # 1. 게시글 발행 작업: 매일 1회 실행
    scheduler.add_job(
        publish_post_job,
        'cron',
        # day='*/2',
        hour=9,
        id='publish_post_job',        
        replace_existing=True,
    )
    
    # 2. 댓글 발행 작업: 매일 1회 실행
    scheduler.add_job(
        publish_comment_job,
        'cron',
        hour=10, 
        minute=5, 
        id='publish_comment_job',     
        replace_existing=True,
    )

    scheduler.start()
    print("Scheduler started...")