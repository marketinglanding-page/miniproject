from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_check = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'name', 'nickname', 'password', 'password_check')

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'nickname', 'phone_number', 'created_at')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError('이메일 또는 비밀번호가 잘못되었습니다.')
        data['user'] = user
        return data
