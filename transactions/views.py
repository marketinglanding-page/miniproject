# transactions/views.py

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    # 1. 사용할 모델의 전체 쿼리셋 정의 (기본 데이터)
    queryset = Transaction.objects.all()

    # 2. 사용할 시리얼라이저 정의
    serializer_class = TransactionSerializer

    # 3. 사용할 백엔드 필터 정의 (필터링 및 정렬 기능)
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # 4. 필터링에 사용할 필드 정의 (필수)
    # transaction_type 필터링, date는 날짜 범위 필터링을 위해 '__gte', '__lte' 사용
    filterset_fields = ['transaction_type', 'amount', 'date']

    # 5. 정렬에 사용할 필드 정의 (선택)
    ordering_fields = ['amount', 'date', 'created_at']
    ordering = ['-date']  # 기본 정렬 기준 설정

    # 6. 추가 필터링 로직 구현 (필요하다면 get_queryset 메소드를 오버라이드하여 구현)
    # def get_queryset(self):
    #     # 예시: 특정 사용자에게 속한 트랜잭션만 필터링 (인증 로직 추가 시)
    #     # return Transaction.objects.filter(user=self.request.user)
    #     return super().get_queryset()


from django.shortcuts import render
