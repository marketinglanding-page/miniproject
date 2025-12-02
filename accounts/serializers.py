from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # user는 자동으로 설정되므로 read_only에 포함
        fields = [
            'id',
            'account_number',
            'bank_code',
            'account_type',
            'name',
            'created_at',
            'user'
        ]
        # user, id, created_at은 조회 전용 필드
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        """
        계좌번호와 은행코드가 사용자별로 고유한지 확인합니다.
        """
        # 현재 뷰에서 현재 사용자(user)를 가져옵니다.
        user = self.context['request'].user

        # 계좌번호와 은행코드가 이미 존재하는지 확인 (새 계좌 생성 시)
        if self.instance is None: # Create operation
            if Account.objects.filter(
                    user=user,
                    account_number=data.get('account_number'),
                    bank_code=data.get('bank_code')
            ).exists():
                raise serializers.ValidationError("이미 존재하는 계좌번호와 은행코드 조합입니다.")

        return data