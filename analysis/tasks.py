from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .utils import analyze_and_visualize
from .models import AnalysisRequest
'''
shared_task 사용 : Celery 인스턴스를 직접 임포트하지 않고 태스크를 정의할 수 있습니다.
                    이는 해당 태스크가 어느 Celery 인스턴스에 의해 실행되든지 상관없음을 의미하며, 
                    라이브러리나 재사용 가능한 앱에 적합합니다.
'''

User = get_user_model()

@shared_task(bind=True)
def perform_analysis_task(self, user_id, period_type, analysis_target):
    """
    지정된 사용자, 기간, 대상을 기준으로 분석을 수행하고 결과를 저장하는 Task.
    스케줄링 또는 API 요청에 의해 호출됩니다.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print(f"User with ID {user_id} not found. Aborting task.")
        return

    today = timezone.localdate()

    if period_type == 'WEEKLY':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period_type == 'MONTHLY':
        # 간단하게 지난 30일로 설정
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        print(f"Invalid period_type: {period_type}")
        return

    # 분석 및 시각화 로직 호출
    image_buffer, summary = analyze_and_visualize(
        user=user,
        start_date=start_date,
        end_date=end_date,
        target=analysis_target
    )

    if image_buffer is None:
        # 데이터가 없는 경우
        print(f"No transactions found for analysis: {summary}")
        return

    # 실제 환경에서는 이미지 버퍼를 AWS S3나 Azure Blob Storage에 저장하고 
    # result_image_url에 저장된 URL을 업데이트해야 합니다.
    # 여기서는 Base64 인코딩된 문자열을 임시로 사용합니다.
    import base64
    image_base64 = base64.b64encode(image_buffer.read()).decode('utf-8')
    image_url = f"data:image/png;base64,{image_base64}"

    # AnalysisRequest 모델 생성 (요구사항 4 반영)
    AnalysisRequest.objects.create(
        user=user,
        analysis_target=analysis_target,
        period_type=period_type,
        start_date=start_date,
        end_date=end_date,
        result_image_url=image_url,
        result_summary=summary
    )

    print(f"Analysis successfully completed for User {user_id} ({period_type}, {analysis_target})")

    return summary # Task 결과로 요약을 반환