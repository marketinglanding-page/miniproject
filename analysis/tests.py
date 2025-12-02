import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

# analysis/utils.py의 핵심 로직 테스트를 위해 mock이 필요합니다.
from unittest.mock import patch, MagicMock

# 임시 Transaction 모델 정의 (실제 transactions.models.Transaction과 동일하게)
# 실제 프로젝트에서는 Transaction 모델을 정상적으로 임포트해야 합니다.
class MockTransaction(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def values(self, *args):
        # Transaction.objects.filter().values(...) 호출을 모방
        return []

    @classmethod
    def filter(cls, *args, **kwargs):
        # .objects.filter() 호출을 모방
        return cls()

# 주의: 실제 환경에서는 transactions.models.Transaction을 사용하세요.
# from transactions.models import Transaction

User = get_user_model()

class AnalysisUtilTest(TestCase):
    def setUp(self):
        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            nickname='테스트유저'
        )
        self.start_date = timezone.localdate() - datetime.timedelta(days=7)
        self.end_date = timezone.localdate()

    @patch('analysis.utils.Transaction') # Transaction 모델을 모의(Mock) 객체로 대체합니다.
    @patch('analysis.utils.pd')         # Pandas를 모의(Mock) 객체로 대체합니다.
    @patch('analysis.utils.plt')        # Matplotlib을 모의(Mock) 객체로 대체합니다.
    def test_analyze_and_visualize_success(self, MockPlot, MockPandas, MockTransaction):
        """
        1. Analyzer가 제대로 데이터 시각화를 수행하고 Analysis 모델을 생성하는지를 확인할 수 있는 테스트 코드를 작성한다.
        - 분석 로직이 정상적으로 실행되고 이미지 버퍼와 요약을 반환하는지 테스트
        """

        # Mocking: 거래 내역이 있다고 가정
        MockTransaction.objects.filter.return_value.values.return_value = [
            {'transaction_timestamp': self.start_date, 'amount': 10000, 'transaction_type': False},
        ]

        # Mocking: DataFrame 생성을 모의
        mock_df = MagicMock()
        mock_df.empty = False
        mock_df.__len__.return_value = 1 # 총 거래 건수 1건
        mock_df.__getitem__.return_value.sum.return_value = -10000 # 총 금액
        MockPandas.DataFrame.return_value = mock_df

        # Mocking: 시각화 함수 (savefig)가 호출되는지 확인

        from analysis.utils import analyze_and_visualize

        image_buffer, summary = analyze_and_visualize(
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            target='EXPENSE'
        )

        # 3. plt.savefig가 호출되었는지 확인 (시각화 성공)
        MockPlot.savefig.assert_called_once()

        # 4. 이미지 버퍼와 요약이 정상적으로 반환되었는지 확인
        self.assertIsNotNone(image_buffer)
        self.assertIn("총 거래 1건", summary)

    @patch('analysis.utils.Transaction')
    def test_analyze_and_visualize_no_data(self, MockTransaction):
        """
        - 거래 내역이 없는 경우 예외 처리가 되는지 테스트
        """

        # Mocking: 거래 내역이 없다고 가정
        MockTransaction.objects.filter.return_value.values.return_value = []

        from analysis.utils import analyze_and_visualize

        image_buffer, summary = analyze_and_visualize(
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            target='ALL'
        )

        # 이미지 버퍼가 None이고 요약이 "거래 내역이 없습니다"인지 확인
        self.assertIsNone(image_buffer)
        self.assertIn("거래 내역이 없습니다", summary)


class AnalysisAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='api_test@example.com',
            password='password123',
            nickname='API테스터'
        )
        self.client.force_authenticate(user=self.user)
        self.url = '/api/analysis/results/' # analysis/urls.py의 name='analysis-list'에 해당하는 URL 가정

    @patch('analysis.views.analyze_and_visualize')
    def test_analysis_list_api_success(self, mock_analyze):
        """
        2. 앞서 구현한 API View에 대한 Test Code 작성하기
        - 유효한 쿼리 파라미터로 API 요청 시, 분석이 수행되고 201 응답을 반환하는지 테스트
        """

        # Mocking: analyze_and_visualize 함수가 성공적으로 이미지와 요약을 반환한다고 가정
        mock_buffer = MagicMock()
        mock_buffer.read.return_value = b'fake_png_data' # 가짜 이미지 데이터
        mock_analyze.return_value = (mock_buffer, "가짜 분석 요약입니다.")

        # 쿼리 파라미터: 지난 7일 지출 분석
        response = self.client.get(
            self.url,
            {'period_type': 'WEEKLY', 'analysis_target': 'EXPENSE'}
        )

        # 1. 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. 분석 함수가 호출되었는지 확인
        mock_analyze.assert_called_once()

        # 3. 응답 데이터 확인
        self.assertIn('result_summary', response.data)
        self.assertEqual(response.data['result_summary'], "가짜 분석 요약입니다.")

    def test_analysis_list_api_unauthenticated(self):
        """
        - 인증되지 않은 사용자가 접근 시 401 Unauthorized를 반환하는지 테스트
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)