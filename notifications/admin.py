# notifications/admin.py

from django.contrib import admin
from .models import Notification, NotificationSetting 

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 사용자, 읽음 여부, 생성일, 메시지 일부
    list_display = (
        'user', 
        'is_read',           # 읽음 여부 (가장 중요한 필터링 대상)
        'created_at', 
        'message_snippet'    # 메시지 미리보기용 커스텀 메서드 사용
    )
    
    # 2. 검색 필드 (search_fields): 사용자 이메일과 메시지 내용으로 검색
    search_fields = (
        'user__email',        
        'message'             # 메시지 본문 검색
    )
    
    # 3. 필터링 (list_filter): 읽음 여부와 생성일로 필터링
    list_filter = (
        'is_read', 
        'created_at'
    )
    
    # 4. 시간 계층 (date_hierarchy): 날짜별 탐색
    date_hierarchy = 'created_at' 
    
    # 5. FK 성능 최적화
    raw_id_fields = ('user',)
    
    # 6. 커스텀 메서드: 메시지 내용을 일정 길이로 잘라 목록에 표시
    @admin.display(description='메시지')
    def message_snippet(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 누가, 어떤 방식으로, 어떤 기준으로 설정했는지
    list_display = (
        'user', 
        'setting_type', 
        'threshold', 
        'is_email_active', 
        'is_app_active'
    )
    
    # 2. 검색 필드 (search_fields): 사용자 이메일과 설정 유형으로 검색
    search_fields = (
        'user__email', 
        'setting_type'
    )
    
    # 3. 필터링 (list_filter): 이메일/앱 활성화 상태 및 설정 유형 필터링
    list_filter = (
        'is_email_active',     # 이메일 활성화 사용자만 보기
        'is_app_active',       # 앱 알림 활성화 사용자만 보기
        'setting_type'
    )
    
    # 4. FK 성능 최적화
    raw_id_fields = ('user',)