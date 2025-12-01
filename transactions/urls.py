from django.urls import path
from .views import AccountTransactionSumView

urlpatterns = [
    # 거래 합계 API 엔드포인트
    path('sum/', AccountTransactionSumView.as_view(), name='transaction-sum'),
]