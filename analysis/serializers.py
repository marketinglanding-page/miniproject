from rest_framework import serializers
from .models import AnalysisRequest

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRequest
        # result_image_url과 result_summary는 분석 후 저장되는 필드
        fields = ['id', 'analysis_target', 'period_type', 'start_date', 'end_date',
                  'result_image_url', 'result_summary', 'created_at']
        read_only_fields = fields # 이 뷰는 목록 반환용이므로 모두 읽기 전용