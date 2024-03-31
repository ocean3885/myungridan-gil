from django.apps import AppConfig

class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'

    def ready(self):
        # signals.py를 여기서 임포트합니다.
        import post.signals
