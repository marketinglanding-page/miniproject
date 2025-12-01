# notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, NotificationSetting
from transactions.models import Transaction 
from analysis.models import AnalysisRequest 
import logging

logger = logging.getLogger(__name__)


# 거래 생성 시 임계값 알림 로직
@receiver(post_save, sender=Transaction)
def check_transaction_threshold(sender, instance, created, **kwargs):
    # 지출 초과 알림 로직
    # 새로 생성된 거래가 아니거나 (수정), '출금'이 아닐 경우 스킵
    if not created or instance.transaction_type != '출금': 
        return

    # Account 모델의 user 필드를 통해 사용자 정보를 가져옵니다.
    try:
        user = instance.account.user 
    except AttributeError:
        logger.error(f"User retrieval failed for transaction {instance.id}")
        return

    try:
        setting = NotificationSetting.objects.get(user=user)
        
        # 앱 알림 활성화 및 금액 임계값 검사
        if setting.is_app_active and instance.amount >= setting.threshold:
            
            message = (
                f"🚨 지출 경고: 기준 금액({setting.threshold:,}원)을 초과하는 "
                f"지출({instance.amount:,}원)이 발생했습니다."
            )
            
            Notification.objects.create(
                user=user,
                message=message,
            )
            logger.info(f"Threshold Alert generated for User {user.id}")

    except NotificationSetting.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Error creating notification for User {user.id}: {e}")


# --- 2. 분석 요청 결과 완료 시 알림 로직 ---
@receiver(post_save, sender=AnalysisRequest)
def send_analysis_notification(sender, instance, created, **kwargs):
    """
    AnalysisRequest 모델이 저장/업데이트될 때 결과 URL이 채워졌으면 알림을 보냅니다.
    (분석 완료 시점을 result_image_url 필드 채워짐으로 간주)
    """
    # 결과 이미지 URL이 아직 채워지지 않았으면 스킵
    if not instance.result_image_url:
        return

    # 사용자는 AnalysisRequest 모델에 직접 연결되어 있습니다.
    user = instance.user 

    try:
        # 알림 메시지 생성 (결과 요약을 포함)
        summary = instance.result_summary if instance.result_summary else "결과 요약 없음"
        message = (
            f"분석 요청({instance.analysis_target} - {instance.period_type}) 결과가 준비되었습니다. "
            f"요약: {summary[:50]}..."
        )
        
        Notification.objects.create(
            user=user,
            message=message,
        )
        logger.info(f"Analysis result notification generated for User {user.id}")

    except Exception as e:
        logger.error(f"Error creating analysis notification for User {user.id}: {e}")