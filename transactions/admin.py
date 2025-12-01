# transactions/admin.py

from django.contrib import admin
from .models import Transaction
# Account 모델이 transactions.models에서 import 되었으므로, 
# 이곳에서는 Transaction 모델만 불러오면 됩니다.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # 1. 목록 표시 (list_display): 핵심 재무 정보와 관계를 한눈에 보게 설정.
    # (account, 금액, 거래 유형, 거래 후 잔액, 일시)
    list_display = (
        'account', 
        'amount', 
        'transaction_type', 
        'balance_after', 
        'transaction_timestamp'
    )
    
    # 2. 검색 필드 (search_fields): 계좌번호 및 상세 내역 검색 활성화
    # 'account__account_number'는 외래키(FK)를 통해 Account 모델의 'account_number' 필드를 검색합니다.
    search_fields = (
        'account__account_number', # 계좌번호로 검색
        'transaction_details'     # 상세 내역으로 검색
    )
    
    # 3. 필터링 (list_filter): 거래 방식 및 유형, 날짜 필터링
    list_filter = (
        'transaction_type',        # 입금/출금 필터링
        'transaction_method',      # 거래 방식 필터링
        'transaction_timestamp',   # 날짜별 필터링
    )
    
    # 4. 시간 계층 (date_hierarchy): 날짜별로 탐색할 수 있는 상위 메뉴 생성 (월별/일별)
    date_hierarchy = 'transaction_timestamp'
    
    # 5. 관계 최적화 (raw_id_fields): FK 조회 성능 최적화
    # 거래가 매우 많을 경우, 계좌(account) 필드를 ID로 입력받아 페이지 로딩을 빠르게 합니다.
    raw_id_fields = ('account',) 
    
    # 6. 정렬 기준 (ordering): 최신 거래 내역 상단표시 설정 (선택 사항, Meta 클래스에 정의됨)
    ordering = ('-transaction_timestamp',)