from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # API에서 사용하고 싶거나 사용자에게 받고 싶은 모든 필드를 포함합니다.
        fields = ['id', 'amount', 'transaction_type', 'description', 'date', 'created_at']
        read_only_fields = ['created_at'] # 생성일은 읽기 전용으로 설정