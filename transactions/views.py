from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction, Account  # Account 모델은 필터링을 위해 필요
from .serializers import TransactionSerializer
import logging

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ## 거래 내역 관리 (Transaction Management)

    로그인한 사용자의 **거래 내역(Transaction)**을 조회, 생성, 필터링 및 정렬하는 ViewSet입니다.

    ### 지원 메서드
    * `GET /transactions/`: 목록 조회 및 필터링
    * `GET /transactions/{pk}/`: 개별 상세 조회
    * `POST /transactions/`: 새 거래 내역 생성

    ### 인증 및 권한
    * **인증 필수:** `IsAuthenticated` (로그인된 사용자만 접근 가능)
    * **소유권 제한:** 사용자는 자신이 소유한 계좌(`account__user`)에 연결된 거래 내역만 조회 및 생성할 수 있습니다.

    ### 생성 시 유의 사항 (POST)
    거래 내역 생성 시, 서버에서 계좌 유효성 검사 및 금액 업데이트 등의 로직이 실행됩니다.
    * **`account` :** 반드시 사용자 본인이 소유한 유효한 계좌 ID를 포함해야 합니다.

    ### 필터링 (Query Parameters)
    `DjangoFilterBackend`를 사용하여 다양한 조건으로 거래 내역을 필터링할 수 있습니다.

    | 필터 필드 | 설명 | 예시 |
    | :--- | :--- | :--- |
    | `account` | 거래가 발생한 특정 계좌 ID로 필터링합니다. | `?account=1` |
    | `transaction_type` | 거래 유형(`DEPOSIT`, `WITHDRAW` 등)으로 필터링합니다. | `?transaction_type=WITHDRAW` |
    | `transaction_method` | 거래 방식(`ATM`, `CARD`, `TRANSFER` 등)으로 필터링합니다. | `?transaction_method=CARD` |
    | `transaction_timestamp` | 특정 일시와 일치하는 거래 내역을 필터링합니다. | `?transaction_timestamp=2025-11-20T10:00:00` |

    ### 정렬 (Ordering)
    `OrderingFilter`를 사용하여 결과를 정렬할 수 있습니다.

    | 정렬 필드 | 설명 |
    | :--- | :--- |
    | `amount` | 거래 금액을 기준으로 정렬합니다. |
    | `transaction_timestamp` | 거래 발생 시간을 기준으로 정렬합니다. |

    **기본 정렬:** `transaction_timestamp` (최신순)
    """
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
