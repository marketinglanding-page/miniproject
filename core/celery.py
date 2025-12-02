import os
from celery import Celery

# 'django' 설정을 Celery 프로그램의 기본값으로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Celery 인스턴스 생성
app = Celery('core')

# Django 설정에서 Celery 설정을 로드합니다.
# Celery 관련 설정은 모두 settings.py의 'CELERY_'로 시작하는 변수에서 가져옵니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# INSTALLED_APPS에서 Task 모듈을 자동으로 검색합니다.
app.autodiscover_tasks()
# 이제 각 앱 폴더의 tasks.py 파일을 자동으로 찾게 됩니다.

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')