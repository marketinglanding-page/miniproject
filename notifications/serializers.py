# notifications/serializers.py

from rest_framework import serializers
from .models import Notification, NotificationSetting

class NotificationSerializer(serializers.ModelSerializer):
    # 데이터 조회기능 담당
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']


class NotificationSettingSerializer(serializers.ModelSerializer):
    # 알림 설정 생성 및 수정 기능 담당
    class Meta:
        model = NotificationSetting
        fields = [
            'setting_type', 
            'threshold', 
            'is_email_active', 
            'is_app_active'
        ]
        # user 필드는 뷰에서 현재 사용자로 자동 설정되므로 read_only로 설정합니다.
        # 단, OneToOneField의 primary_key이므로 fields에서 명시적으로 제외했습니다.