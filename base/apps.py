from django.apps import AppConfig

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    
    def ready(self):
    # Django가 준비되면 스케줄러를 시작합니다.
    # 개발 서버(runserver)는 리로딩 때문에 코드가 두 번 실행될 수 있습니다.
        # from . import scheduler
        # scheduler.start()
        pass
