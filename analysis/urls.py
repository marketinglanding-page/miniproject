from django.urls import path
from .views import AnalysisResultListView

urlpatterns = [
    # GET /analysis/?period_type=WEEKLY&analysis_target=EXPENSE
    path('results/', AnalysisResultListView.as_view(), name='analysis-list'),
]