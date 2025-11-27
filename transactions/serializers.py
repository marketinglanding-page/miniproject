from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # API 입출력에 사용할 필드  목록
        fields = ['id', 'amount', 'transaction_type', 'description', 'date', 'created_at'] 
        read_only_fields = ['created_at']