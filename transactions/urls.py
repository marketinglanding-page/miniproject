# transactions/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TransactionViewSet

router = DefaultRouter()

# TransactionViewSet에 정의된 CRUD 경로를 /api/v1/transactions/ 경로에 연결합니다.
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]