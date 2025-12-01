# common/admin.py

from django.contrib import admin
from .models import CommonCode

@admin.register(CommonCode)
class CommonCodeAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 분류, 코드, 설명을 한눈에
    list_display = (
        'category',       # 분류별 그룹화가 핵심
        'code',           
        'description',
        'id'              # ID를 함께 표시하여 디버깅 편의성 확보
    )
    
    # 2. 검색 필드 (search_fields): 분류, 코드, 설명 모두 검색 가능하도록 설정
    search_fields = (
        'category',       # 분류명으로 검색
        'code',           # 코드값으로 검색
        'description'     # 설명으로 검색
    )
    
    # 3. 필터링 (list_filter): 분류(category)를 기준으로 필터링
    list_filter = (
        'category',       # 목록 페이지 오른쪽에 분류별 필터 박스 생성
    )
    
    # 4. 목록 편집 (list_editable): 목록 페이지에서 바로 수정 가능하도록 설정
    # 코드 분류는 고정하고 설명은 즉시 수정할 수 있도록 설정
    list_editable = (
        'description',
    )