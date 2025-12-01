from rest_framework import serializers

class TransactionSumSerializer(serializers.Serializer):
    """특정 기간의 거래 합계를 반환하기 위한 Serializer"""
    account_name = serializers.CharField(max_length=60, label="계좌별칭")
    start_date = serializers.DateField(label="시작일")
    end_date = serializers.DateField(label="종료일")
    total_amount = serializers.IntegerField(label="총 거래 금액")