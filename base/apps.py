from django.apps import AppConfig
import os

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    
    def ready(self):
    # Django가 준비되면 스케줄러를 시작합니다.
    # 개발 서버(runserver)는 리로딩 때문에 코드가 두 번 실행될 수 있습니다.
    # 운영 환경에서는 이런 문제가 없으므로, os.environ.get('RUN_MAIN') 등으로 
    # 한 번만 실행되도록 하는 트릭을 사용하기도 합니다.
        if os.environ.get('RUN_MAIN'):
            from . import scheduler
            scheduler.start()
