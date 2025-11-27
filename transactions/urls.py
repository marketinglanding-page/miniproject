from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

# Router 객체  생성
router = DefaultRouter()

# ViewSet을 'transactions' 경로에 등록
# 예시 엔드포인트: /api/v1/transactions/
router.register(r'', TransactionViewSet, basename='transaction')

# router의 모든 URL을 반환합니다.
urlpatterns = router.urls