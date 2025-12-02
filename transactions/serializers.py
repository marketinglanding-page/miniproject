from rest_framework import serializers
from django.db import transaction as db_transaction
from django.utils import timezone
from .models import Transaction
from accounts.models import Account
from common.models import CommonCode  # CommonCode 모델을 사용하여 유효성 검사


class TransactionSerializer(serializers.ModelSerializer):
    # 1. 입력용: 계좌 PK만 받습니다.
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='account',
        write_only=True,
        error_messages={'does_not_exist': '선택된 계좌 ID가 존재하지 않습니다.'}
    )
    # 2. 출력용: 계좌 별칭을 보여줍니다.
    account_name = serializers.CharField(source='account.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'account_id', 'account_name',
            'transaction_type', 'transaction_method',
            'amount', 'transaction_details', 'transaction_timestamp',
            'balance_after'
        ]
        read_only_fields = ['id', 'balance_after', 'account_name']

    def validate(self, data):
        user = self.context['request'].user
        account = data.get('account')

        # 1. 계좌 소유권 검증 (보안)
        if account and account.user != user:
            raise serializers.ValidationError({"account_id": "선택된 계좌는 현재 사용자의 소유가 아닙니다."})

        # 2. CommonCode 유효성 검증 (데이터 일관성)
        type_code = data.get('transaction_type')
        method_code = data.get('transaction_method')

        if not CommonCode.objects.filter(category='TRANSACTION_TYPE', code=type_code).exists():
            raise serializers.ValidationError({"transaction_type": f"유효하지 않은 거래 유형 '{type_code}'입니다."})

        if not CommonCode.objects.filter(category='TRANSACTION_METHOD', code=method_code).exists():
            raise serializers.ValidationError({"transaction_method": f"유효하지 않은 거래 방식 '{method_code}'입니다."})

        # 3. 날짜 검증
        if data.get('transaction_timestamp') and data.get('transaction_timestamp') > timezone.now():
            raise serializers.ValidationError({"transaction_timestamp": "거래일시는 미래 시점일 수 없습니다."})

        return data

    def create(self, validated_data):
        account = validated_data['account']
        transaction_type = validated_data['transaction_type']
        amount = validated_data['amount']

        # 동시성 제어 및 무결성 확보: DB 트랜잭션 블록 사용
        with db_transaction.atomic():
            # 최신 잔액 조회 (Transaction.objects.order_by('-transaction_timestamp').first()와 동일)
            latest_transaction = Transaction.objects.filter(account=account).first()
            current_balance = latest_transaction.balance_after if latest_transaction else 0

            # 잔액 계산
            if transaction_type == '출금':
                new_balance = current_balance - amount
                if new_balance < 0:
                    # 잔액 부족 시 트랜잭션 롤백 및 에러 반환
                    raise serializers.ValidationError({"amount": f"잔액({current_balance:,}원)이 부족하여 출금할 수 없습니다."})
            elif transaction_type == '입금':
                new_balance = current_balance + amount
            else:
                new_balance = current_balance

            validated_data['balance_after'] = new_balance
            transaction = super().create(validated_data)

            return transaction
