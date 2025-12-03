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
    ## 알림 목록 조회

    로그인한 사용자의 **전체 알림 목록**을 최신순(created_at 기준)으로 조회하는 엔드포인트입니다.

    ### 특징
    * **인증 필수:** 로그인된 사용자만 접근할 수 있습니다.
    * **정렬:** 알림은 가장 최근에 생성된 순서로 정렬되어 반환됩니다.
    * **읽음 상태:** 알림의 `is_read` 필드를 통해 사용자가 해당 알림을 읽었는지 여부를 확인할 수 있습니다.

    ---
    **개별 알림 읽음 처리:**
    특정 알림을 읽음으로 표시하려면 `/notifications/{pk}/read/` 엔드포인트를 사용하십시오.
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
    ## 알림 설정 관리

    현재 로그인한 사용자의 알림 설정을 **조회(GET)**하고 **수정(PUT/PATCH)**할 수 있는 엔드포인트입니다.

    ### 특징
    * **GET 요청 시:** 사용자의 설정이 존재하지 않으면, 임계값 100,000원의 기본 설정이 자동으로 생성됩니다.
    * **PUT/PATCH 요청 시:** 알림 수신 여부(`is_active`)나 임계값(`threshold`) 등을 수정할 수 있습니다.
    * **수정 제한:** `setting_type` 필드는 보안상의 이유로 수정할 수 없습니다.

    ---
    **Example Body (PATCH):**
    ```json
    {
        "is_active": false,
        "threshold": 50000
    }
    ```
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
    ## ✅ 개별 알림 읽음 처리

    URL 경로에 지정된 **특정 알림(PK)**의 `is_read` 상태를 **True**로 변경합니다.

    이 엔드포인트는 알림 목록에서 사용자가 특정 항목을 눌렀을 때 사용됩니다.

    ### 요청 방식
    * **권장:** `PATCH` 요청을 사용하여 `is_read` 필드만 업데이트하는 것이 가장 효율적입니다.
    * **URL:** `/notifications/{pk}/read/`

    ### 응답
    * **200 OK:** 알림이 성공적으로 읽음 처리된 경우.
    * **404 NOT FOUND:** 해당 PK를 가진 알림이 없거나, 현재 사용자에게 속하지 않은 경우.
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