import base64
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import AnalysisRequest
from .serializers import AnalysisSerializer
from .utils import analyze_and_visualize
from rest_framework.permissions import IsAuthenticated

class AnalysisResultListView(generics.ListAPIView):
    """
    5. 응답으로 분석 결과 리스트를 반환해주는 API View
    6. 쿼리 파라미터를 이용해서 기간 별로(주간, 월간) 분석 데이터를 가지고 옴
    """
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated] # 인증된 사용자만 접근 가능하다고 가정

    def get_queryset(self):
        # 현재 사용자의 분석 요청 기록만 필터링
        return AnalysisRequest.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        # 쿼리 파라미터로 기간 정보 추출
        period = request.query_params.get('period_type', 'MONTHLY') # 기본값: 월간

        # 쿼리 파라미터로 분석 대상 추출
        target = request.query_params.get('analysis_target', 'ALL').upper()

        today = timezone.localdate()

        if period == 'WEEKLY':
            # 지난 7일 (주간)
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == 'MONTHLY':
            # 지난 30일 (월간)
            start_date = today - timedelta(days=30)
            end_date = today
        else:
            return Response({"detail": "유효하지 않은 period_type 값입니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 1. 기존 분석 기록 확인 (선택 사항: 재분석 방지)
        # 이미 이 기간과 대상으로 분석한 기록이 있다면 그 결과를 반환할 수 있음.
        existing_result = self.get_queryset().filter(
            period_type=period,
            analysis_target=target,
            start_date__gte=start_date,
            end_date__lte=end_date
        ).first()

        if existing_result:
            serializer = self.get_serializer(existing_result)
            return Response(serializer.data)

        # 2. 분석 로직 실행 (utils.py)
        image_buffer, summary = analyze_and_visualize(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            target=target
        )

        if image_buffer is None:
            return Response({"detail": summary},
                            status=status.HTTP_204_NO_CONTENT)

        # 3. 이미지 저장 및 URL 생성 (임시로 Base64 인코딩)
        # 실제 환경에서는 AWS S3 등에 저장하고 URL을 받아와야 합니다.
        image_base64 = base64.b64encode(image_buffer.read()).decode('utf-8')
        image_url = f"data:image/png;base64,{image_base64}"

        # 4. AnalysisRequest 모델 생성 및 저장
        new_analysis = AnalysisRequest.objects.create(
            user=request.user,
            analysis_target=target,
            period_type=period,
            start_date=start_date,
            end_date=end_date,
            result_image_url=image_url, # 실제 URL로 대체 필요
            result_summary=summary
        )

        serializer = self.get_serializer(new_analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)