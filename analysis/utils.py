import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models import Q
from transactions.models import Transaction

def analyze_and_visualize(user, start_date, end_date, target):
    """
    1. 기간별 거래 내역을 가져와 Pandas DataFrame 생성
    2. 데이터프레임을 Matplotlib으로 시각화
    3. 시각화된 그래프를 이미지(BytesIO)로 저장
    """

    # 1. 기간 및 사용자별 거래 내역 가져오기
    # 거래 유형 필터링 (target: 'INCOME', 'EXPENSE', 'ALL')
    if target == 'INCOME':
        filter_q = Q(transaction_type=True) # True: 입금(Income)이라고 가정
    elif target == 'EXPENSE':
        filter_q = Q(transaction_type=False) # False: 출금(Expense)이라고 가정
    else:
        filter_q = Q() # 전체

    transactions_queryset = Transaction.objects.filter(
        filter_q,
        account__user=user,
        transaction_timestamp__range=[start_date, end_date]
    ).values('transaction_timestamp', 'amount', 'transaction_type')

    # 데이터프레임 생성
    df = pd.DataFrame(list(transactions_queryset))

    if df.empty:
        return None, "분석 기간 동안 거래 내역이 없습니다."

    # 데이터 전처리: 날짜 인덱싱 및 금액 부호 조정 (지출은 음수로)
    df['date'] = pd.to_datetime(df['transaction_timestamp']).dt.date
    df['signed_amount'] = df.apply(
        lambda row: -row['amount'] if row['transaction_type'] == False else row['amount'],
        axis=1
    )

    # 2. 데이터 시각화 (예: 일별/주별 금액 합계)
    df_daily = df.groupby('date')['signed_amount'].sum()

    plt.figure(figsize=(10, 5))
    df_daily.plot(kind='bar')
    plt.title(f"{user.nickname}의 {start_date} ~ {end_date} 거래 분석 ({target})")
    plt.xlabel("날짜")
    plt.ylabel("금액 (원)")
    plt.grid(axis='y')
    plt.tight_layout()

    # 3. 시각화 된 그래프는 이미지(BytesIO)로 저장
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close() # 메모리 해제

    buffer.seek(0)

    # 간략한 결과 요약 생성
    summary = f"총 거래 {len(df)}건. 합계 금액: {df['signed_amount'].sum():,.0f}원."

    return buffer, summary