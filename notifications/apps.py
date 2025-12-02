# notifications/apps.py

from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = '알림 관리'
    
    def ready(self):
        # 이 한 줄이 'notifications/signals.py'를 로드하고
        # 트랜잭션 저장 시 알림을 생성하는 로직을 활성화합니다.
        import notifications.signals