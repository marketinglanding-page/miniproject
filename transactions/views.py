from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Sum
from accounts.models import Account # accounts 앱의 Account 모델 임포트
from .models import Transaction
from .serializers import TransactionSumSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime

class AccountTransactionSumView(APIView):
    """
    특정 계좌의 특정 기간 동안의 거래 금액 합계를 계산하는 API
    URL: /api/v1/transactions/sum/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. 필수 파라미터 가져오기
        account_name = request.query_params.get('account_name')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not all([account_name, start_date_str, end_date_str]):
            return Response(
                {"detail": "account_name, start_date, end_date 파라미터는 필수입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 날짜 형식 변환 및 유효성 검사 (YYYY-MM-DD 형식 권장)
        try:
            # 예시: 2025-10-01 형식
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            # 종료일은 해당 날짜의 23:59:59까지 포함해야 정확함
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"detail": "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식을 사용하세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. 계좌 조회 및 소유자 확인
        # 현재 인증된 사용자가 소유한 계좌 중에서 계좌 이름이 일치하는 것을 찾습니다.
        try:
            account = get_object_or_404(
                Account,
                user=request.user,
                name=account_name
            )
        except:
            return Response(
                {"detail": f"'{account_name}' 이라는 계좌를 찾을 수 없거나 접근 권한이 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 4. 거래 내역 합계 계산
        # 필터 조건: 해당 계좌(account)와 거래 일시(transaction_timestamp) 범위
        summary = Transaction.objects.filter(
            account=account,
            transaction_timestamp__date__gte=start_date, # 시작일보다 크거나 같음
            transaction_timestamp__date__lte=end_date,   # 종료일보다 작거나 같음
        ).aggregate(
            # BigIntegerField인 amount 필드의 합계를 구합니다.
            total=Sum('amount')
        )

        total_amount = summary['total'] if summary['total'] is not None else 0

        # 5. 결과 반환
        response_data = {
            "account_name": account_name,
            "start_date": start_date,
            "end_date": end_date,
            "total_amount": total_amount,
        }

        # Serializer를 사용하여 최종 출력 형식 확인
        serializer = TransactionSumSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)