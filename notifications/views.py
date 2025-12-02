# notifications/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationSetting
from .serializers import NotificationSerializer, NotificationSettingSerializer
import logging

logger = logging.getLogger(__name__)


# 1. 알림 목록 조회 및 읽음 처리
class NotificationListAPIView(generics.ListAPIView):
    """
    로그인한 사용자의 알림 목록을 조회하고, 특정 알림을 '읽음'으로 처리하는 뷰
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 현재 사용자에게 속한 알림만 최신순으로 반환합니다.
        # models.py에서 ordering = ['-created_at']로 설정했으므로, 그 순서를 따릅니다.
        return Notification.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # 기본 목록 조회 기능
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 2. 알림 설정 조회 및 수정
class NotificationSettingAPIView(generics.RetrieveUpdateAPIView):
    """
    현재 사용자의 알림 설정을 조회하고 (GET), 수정합니다 (PUT/PATCH).
    """
    serializer_class = NotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # OneToOneField로 연결된 NotificationSetting 객체를 가져오는 특별한 메서드
    def get_object(self):
        user = self.request.user
        
        # 설정이 없으면 기본 설정으로 새로 생성합니다 (get_or_create 사용).
        # 이 때 setting_type은 'DEFAULT'로 가정합니다.
        obj, created = NotificationSetting.objects.get_or_create(
            user=user,
            defaults={'setting_type': 'DEFAULT', 'threshold': 100000} # 기본 임계값 10만원 설정
        )
        return obj

    def update(self, request, *args, **kwargs):
        # 업데이트 요청 시, setting_type을 수정하지 못하도록 방지
        if 'setting_type' in request.data:
            return Response(
                {"detail": "setting_type은 수정할 수 없습니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


# 3. 개별 알림 읽음 처리 (별도 API)
class NotificationMarkAsReadAPIView(generics.UpdateAPIView):
    """
    특정 알림 (PK 기반)의 is_read 필드를 True로 업데이트합니다.
    """
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_object(self):
        # URL에서 PK를 가져와 현재 사용자에게 속한 알림인지 확인합니다.
        return get_object_or_404(
            Notification.objects.filter(user=self.request.user), 
            pk=self.kwargs['pk']
        )
        
    def perform_update(self, serializer):
        # is_read 필드만 True로 강제 업데이트
        serializer.instance.is_read = True
        serializer.instance.save(update_fields=['is_read'])
        
# 참고: 이 뷰는 HTTP PUT 요청이 아닌 PATCH 요청을 사용하도록 클라이언트와 협의해야 합니다.