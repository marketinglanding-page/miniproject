from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction, Account  # Account 모델은 필터링을 위해 필요
from .serializers import TransactionSerializer
import logging

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.select_related('account')

        queryset = queryset.filter(account__user=user)

        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise e
        except Exception as e:
            logger.error(f"Transaction creation failed: {e}")
            raise ValidationError({"detail": "거래 내역 생성 중 알 수 없는 오류가 발생했습니다."})

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = [
        'account',  # 계좌 ID로 필터링
        'transaction_type',  # 입금/출금 유형 필터링
        'transaction_method',  # 거래 방식 필터링
        'transaction_timestamp',  # 특정 일시 일치 필터링
    ]

    ordering_fields = [
        'amount',
        'transaction_timestamp',
    ]
    ordering = ['-transaction_timestamp']
