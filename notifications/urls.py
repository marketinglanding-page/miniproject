# notifications/urls.py

from django.urls import path
from .views import (
    NotificationListAPIView, 
    NotificationSettingAPIView, 
    NotificationMarkAsReadAPIView
)

urlpatterns = [
    # GET: 알림 목록 조회
    path('', NotificationListAPIView.as_view(), name='notification-list'),
    
    # GET, PUT/PATCH: 알림 설정 조회 및 수정
    path('settings/', NotificationSettingAPIView.as_view(), name='notification-settings'),
    
    # PATCH: 특정 알림을 읽음으로 표시 (notifications/1/read/)
    path('<int:pk>/read/', NotificationMarkAsReadAPIView.as_view(), name='notification-mark-read'),
]