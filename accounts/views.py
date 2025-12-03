# accounts/views.py

from rest_framework import viewsets, permissions, mixins
from .models import Account
from .serializers import AccountSerializer

# ModelViewSet 대신 GenericViewSet과 필요한 믹스인(Mixin)을 조합하여 사용
class AccountViewSet(
    # List (GET /accounts/)
    mixins.ListModelMixin,
    # Retrieve (GET /accounts/{id}/)
    mixins.RetrieveModelMixin,
    # Create (POST /accounts/)
    mixins.CreateModelMixin,
    # Destroy (DELETE /accounts/{id}/)
    mixins.DestroyModelMixin,

    # 기본 ViewSet 기능 상속
    viewsets.GenericViewSet
):
    """
    ## 자산 계좌 관리 (Account Management) - CRD 전용

    이 엔드포인트는 로그인한 사용자가 자신의 자산 계좌를
    생성(POST), 조회(GET), 삭제(DELETE)만 할 수 있도록 제공합니다.
    **계좌 정보 수정(PUT/PATCH)은 불가능합니다.**

    ### 특징
    * **작업:** CREATE (POST), READ (GET), DELETE (DELETE)
    * **인증 필수:** 로그인된 사용자만 접근할 수 있습니다.
    * **소유권 관리:** 각 사용자는 자신의 계좌만 생성, 조회, 삭제할 수 있습니다.
    ---
    **URL 패턴:**
    * `GET /accounts/`: 모든 계좌 목록 조회 (R)
    * `POST /accounts/`: 새로운 계좌 생성 (C)
    * `GET /accounts/{id}/`: 특정 계좌 상세 조회 (R)
    * `DELETE /accounts/{id}/`: 특정 계좌 삭제 (D)
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인된 사용자의 Account만 필터링하여 생성일 기준 내림차순으로 반환합니다.
        """
        return Account.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        계좌 생성(POST 요청) 시 user 필드를 자동으로 현재 사용자로 설정합니다.
        """
        serializer.save(user=self.request.user)