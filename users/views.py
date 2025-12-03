from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

# 회원가입
class RegisterAPIView(APIView):
    """
    ## 회원가입 (User Registration)

    새로운 사용자 계정을 생성합니다.

    ### 지원 메서드
    * `POST /users/register/`: 회원가입 처리

    ### 권한
    * `AllowAny` (인증 없이 접근 가능)
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="회원가입",
        request=RegisterSerializer,
        responses={201: OpenApiResponse(response=RegisterSerializer)},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': '회원가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 토큰 발급
class MyTokenObtainPairView(TokenObtainPairView):
    """
    ## 토큰 발급 (Token Obtain)

    이메일과 비밀번호를 통해 인증하고, JWT Access Token 및 Refresh Token을 발급받습니다.

    ### 지원 메서드
    * `POST /users/login/`: 토큰 발급 처리
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="로그인 및 토큰 발급",
        description="인증 성공 시 Access Token (단기)과 Refresh Token (장기)을 반환합니다.",
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(
                description='토큰 발급 성공',
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string', 'description': '접근 토큰 (Access Token)'},
                        'refresh': {'type': 'string', 'description': '갱신 토큰 (Refresh Token)'},
                    }
                }
            ),
            401: OpenApiResponse(description='인증 실패')
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# 리프레시 토큰 엔드포인트
    """
    ## 토큰 갱신 (Token Refresh)

    만료된 Access Token을 갱신하기 위해 유효한 Refresh Token을 사용하여 새로운 Access Token을 발급받습니다.

    ### 지원 메서드
    * `POST /users/token/refresh/`: 토큰 갱신 처리
    """
class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Access Token 갱신",
        description="Refresh Token을 요청 본문에 포함하여 새로운 Access Token을 발급받습니다.",
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(
                description='토큰 갱신 성공',
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string', 'description': '새 접근 토큰 (Access Token)'},
                        # Refresh 토큰은 기본적으로 갱신되지 않습니다.
                    }
                }
            ),
            401: OpenApiResponse(description='유효하지 않거나 만료된 Refresh Token')
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# 로그아웃
class LogoutAPIView(APIView):
    """
    ##  로그아웃 (User Logout)

    제공된 Refresh Token을 블랙리스트에 등록하여 더 이상 사용할 수 없게 만듭니다.

    ### 지원 메서드
    * `POST /users/logout/`: 로그아웃 처리
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="로그아웃 및 토큰 무효화",
        description="Refresh Token을 블랙리스트에 추가하여 사용자 세션을 종료합니다.",
        request={'type': 'object', 'properties': {'refresh': {'type': 'string', 'description': '블랙리스트에 등록할 Refresh Token'}}},
        responses={
            204: OpenApiResponse(description='로그아웃 성공 (No Content)'),
            400: OpenApiResponse(description='refresh token이 누락되었거나 유효하지 않음')
        }
    )

    @extend_schema(
        request=None,
        responses={204: OpenApiResponse(description='Logged out')}
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'refresh token 필요'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail': '유효한 refresh token이 아님'}, status=status.HTTP_400_BAD_REQUEST)
