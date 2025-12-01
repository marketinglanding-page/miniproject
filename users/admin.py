# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TokenBlacklist
from django.utils.translation import gettext_lazy as _ # 다국어 지원

# 1. Custom UserAdmin 정의: Django 기본 UserAdmin 기능을 확장
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 목록 표시: email을 맨 앞에 배치
    list_display = (
        'email', 
        'nickname', 
        'name', 
        'is_active', 
        'is_staff', 
        'date_joined'
    )
    
    # 검색 필드: email, name, nickname으로 검색 활성화 (관리자 검색 효율성)
    search_fields = ('email', 'name', 'nickname', 'phone_number')
    
    # 필터링: 사용자 활성화 상태, 스태프 여부, 가입일로 필터링
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    # 필드셋 커스터마이징: 기본 필드셋에 추가한 필드들을 통합
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # email을 ID로 사용
        (_('Personal info'), {'fields': ('name', 'nickname', 'phone_number')}), # 추가필드
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # 추가필드는 Detail View에서 쉽게 볼 수 있도록 'add_fieldsets'에도 추가
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'nickname', 'phone_number')}),
    )

    # 기본 username 필드를 제거했으므로, filtering_queryset 메서드를 오버라이드하여 username 관련 필터링을 제거할 수 있습니다.
    # (선택 사항: 복잡도를 위해 생략)
    
    # ordering: 최신 가입자가 위에 오도록 설정
    ordering = ('-date_joined',)

@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    # 목록 표시: 토큰 값 대신 생성일을 중심으로 관리
    list_display = (
        'token_snippet',     # 토큰 미리보기용 커스텀 메서드 사용
        'created_at'
    )
    
    # 검색 필드: 토큰 전체 값으로 검색 (매우 긴 값이라 사용 빈도는 낮음)
    search_fields = ('token',)
    
    # 필터링: 생성일 필터링 (언제 블랙리스트에 추가되었는지 확인)
    list_filter = ('created_at',)
    
    # 시간 계층 탐색
    date_hierarchy = 'created_at'
    
    # 커스텀 메서드: 토큰 내용을 일부만 잘라서 표시
    @admin.display(description='토큰')
    def token_snippet(self, obj):
        return obj.token[:30] + '...' if len(obj.token) > 30 else obj.token