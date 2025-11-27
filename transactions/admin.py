from django.contrib import admin
from .models import Transaction


# 1. Transaction 모델의 Admin 표시 형식을 정의합니다.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Admin 목록 페이지에 표시될 필드들 (사용자 ID 대신 'id'를 예시로 사용)
    list_display = (
        'id',
        'amount',
        'transaction_type',
        'description',
        'date',
        'created_at'
    )

    # 목록 페이지 우측에 필터링 옵션을 추가합니다.
    # 거래 유형별, 날짜별로 쉽게 데이터를 분류할 수 있게 됩니다.
    list_filter = (
        'transaction_type',
        'date'
    )

    # 검색창을 활성화하고, 해당 필드에서 검색합니다.
    # 내용(description)과 거래 금액(amount)으로 검색이 가능해집니다.
    search_fields = (
        'description',
        'amount'
    )

    # 날짜 필드(date)를 기준으로 계층적 탐색(년/월/일) 기능을 활성화합니다.
    date_hierarchy = 'date'

    # 상세 보기/수정 페이지에서 필드들의 순서와 그룹을 지정할 수 있습니다.
    fieldsets = (
        (None, {
            'fields': ('amount', 'transaction_type', 'description', 'date')
        }),
        ('메타 정보', {
            # 'classes': ('collapse',), # 이 필드셋을 접을 수 있게 설정
            'fields': ('created_at',),
            'description': '데이터 생성 시간은 자동으로 기록됩니다.'
        })
    )

    # created_at 필드는 읽기 전용으로 설정합니다.
    readonly_fields = ('created_at',)