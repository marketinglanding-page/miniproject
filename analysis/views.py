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
    ## 지출 및 예산 분석 결과 조회 및 요청

    이 엔드포인트는 사용자가 **특정 기간(주간/월간)** 및 **대상(지출/수입/전체)**에 대한
    재무 분석 결과를 조회하거나 새로운 분석을 요청하는 기능을 제공합니다.

    ### 주요 기능
    1.  **기록 조회:** 이미 수행된 분석 기록(AnalysisRequest) 목록을 반환합니다.
    2.  **분석 요청:** 쿼리 파라미터를 사용하여 요청 시, 즉시 분석을 수행하고 그 결과를 `201 Created`로 반환합니다.

    ### 쿼리 파라미터 (분석 요청 시 필수)

    | 파라미터 이름 | 설명 | 필수 여부 | 예시 값 |
    | :--- | :--- | :--- | :--- |
    | `period_type` | 분석 기간 유형 | 선택 (기본값: `MONTHLY`) | `WEEKLY`, `MONTHLY` |
    | `analysis_target` | 분석 대상 항목 | 선택 (기본값: `ALL`) | `EXPENSE`, `INCOME`, `ALL` |

    ### 응답 상태 코드

    * **`200 OK`**: 기존에 저장된 분석 결과를 목록으로 반환할 때.
    * **`201 CREATED`**: 요청된 기간/대상에 대해 **새로운 분석**을 수행하고 결과를 반환했을 때.
    * **`204 NO CONTENT`**: 분석은 수행되었으나 해당 기간에 거래 내역이 없어 결과를 생성할 수 없을 때. (본문에 `detail` 메시지 포함)
    * **`400 BAD REQUEST`**: `period_type` 등 쿼리 파라미터 값이 유효하지 않을 때.
    * **`401 UNAUTHORIZED`**: 인증되지 않은 사용자가 접근했을 때.
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