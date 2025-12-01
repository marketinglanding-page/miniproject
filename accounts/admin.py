# accounts/admin.py (최종 수정 - New ERD 반영)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account  # Custom User 모델 불러오기

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Admin 페이지에서 볼 수 있는 필드 목록
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')

    # 목록 페이지에서 검색 가능한 필드 지정
    search_fields = ('email', 'first_name', 'last_name')

    # 목록 페이지에서 필터링할 수 있는 항목 지정
    list_filter = ('is_staff', 'is_active', 'date_joined')

    # 필드셋을 커스터마이징하여 정보의 구조를 정리할 수 있습니다.
    # (예: UserAdmin의 fieldsets를 상속받아 custom 필드를 추가하는 방식)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('some_custom_field',)}), # 만약 custom 필드가 있다면 추가
    )

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # 1. list_display: 새로운 필드 (bank_code, account_type) 포함
    list_display = (
        'user', 
        'name', 
        'account_number', 
        'bank_code', 
        'account_type', 
        'created_at'
    )
    
    # 2. search_fields: 사용자 이메일과 계좌 정보로 검색
    # User 모델에 email 필드가 있으므로 user__email로 검색 가능
    search_fields = ('user__email', 'account_number', 'name') 
    
    # 3. list_filter: 은행 코드, 계좌 종류, 생성일로 필터링
    list_filter = ('account_type', 'bank_code', 'created_at') 
    
    # 4. raw_id_fields: FK 성능 최적화
    raw_id_fields = ('user',)