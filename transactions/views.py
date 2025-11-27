from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    # 쿼리셋: 모든 Transaction  객체
    queryset = Transaction.objects.all()

    # 시리얼라이저: TransactionSerializer 사용
    serializer_class = TransactionSerializer

    # 필터링 및 정렬 백엔드 활성화
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # ⭐️ 필터링을 허용할 필드 목록 정의
    # 예시: ?transaction_type=INCOME
    filterset_fields = ['transaction_type', 'amount', 'date']

    # ⭐️ 정렬을 허용할 필드 목록 정의
    # 예시: ?ordering=-amount (금액 내림차순 정렬)
    ordering_fields = ['amount', 'date', 'created_at']
    ordering = ['-date']  # 기본 정렬: 날짜 최신순