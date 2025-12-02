from django.db import models
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

class Notification(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="사용자"
    )
    message = models.TextField(verbose_name="메시지")
    is_read = models.BooleanField(verbose_name="읽음 여부", default=False)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = '알림'
        ordering = ['-created_at']


class NotificationSetting(models.Model):
    user = models.OneToOneField(    # 1:1 관계
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="사용자"
    )
    setting_type = models.CharField(verbose_name="설정 유형", max_length=50)     # # common code에 명시할 코드를 미리 적어놓으시는거 추천드립니다.
    threshold = models.BigIntegerField(verbose_name="기준 금액(원 단위)")
    is_email_active = models.BooleanField(verbose_name="이메일 알림 활성화", default=False)
    is_app_active = models.BooleanField(verbose_name="앱 알림 활성화", default=True)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        db_table = 'notification_settings'
        verbose_name = '알림 설정'