from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter()
router.register(r'', AccountViewSet, basename='account')

# /budget/accounts/ (GET, POST)
# /budget/accounts/{pk}/ (GET, PUT, PATCH, DELETE)
urlpatterns = router.urls