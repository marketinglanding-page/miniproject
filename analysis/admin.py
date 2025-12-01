# analysis/admin.py

from django.contrib import admin
from .models import AnalysisRequest, AnalysisSchedule 

@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 핵심 정보 요약
    list_display = (
        'user', 
        'analysis_target', 
        'period_type', 
        'start_date', 
        'end_date',
        'created_at' 
    )
    
    # 2. 검색 필드 (search_fields): 사용자 이메일, 분석 대상, 요약 결과 검색
    search_fields = (
        'user__email',            # FK 관계를 활용한 이메일 검색
        'analysis_target',        
        'result_summary'          
    )
    
    # 3. 필터링 (list_filter): 요청 유형 및 기간 유형 필터링
    list_filter = (
        'analysis_target', 
        'period_type', 
        'created_at'
    )
    
    # 4. 시간 계층 (date_hierarchy): 날짜별 탐색 활성화
    date_hierarchy = 'created_at' 
    
    # 5. 관계 최적화 (raw_id_fields): FK 성능 최적화
    raw_id_fields = ('user',)

@admin.register(AnalysisSchedule)
class AnalysisScheduleAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 활성화 여부를 맨 앞에 배치
    list_display = (
        'is_active',       # 활성화 여부 (가장 중요한 관리 포인트)
        'user', 
        'schedule_type', 
        'run_day'
    )
    
    # 2. 검색 필드 (search_fields): 사용자 이메일 및 스케줄 유형으로 검색
    search_fields = (
        'user__email', 
        'schedule_type'
    )
    
    # 3. 필터링 (list_filter): 활성화 상태와 실행 요일 필터링
    list_filter = (
        'is_active',       
        'schedule_type', 
        'run_day'
    )
    
    # 4. 관계 최적화 (raw_id_fields): OneToOneField 성능 최적화
    raw_id_fields = ('user',)