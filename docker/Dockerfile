# 1단계: 빌드 환경 (Poetry를 사용한 의존성 관리)
# 🔑 Python 버전을 3.13으로 사용합니다.
FROM python:3.13-slim as builder

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# 💡 Poetry가 시스템에 설치될 경로를 PATH에 추가
ENV PATH="$POETRY_HOME/bin:$PATH"

# Poetry 설치 (최신 버전 사용)
RUN pip install poetry==1.8.2

# 작업 디렉토리 설정
WORKDIR /app

# PostgreSQL 및 Pandas 설치를 위한 빌드 도구 설치
# **IMPORTANT**: Pandas와 같은 복잡한 라이브러리 설치를 위해 필수적인 패키지들을 설치합니다.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    gfortran \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Poetry 파일을 복사하고 의존성 설치
COPY pyproject.toml poetry.lock /app/
# 🚨 핵심 수정: --no-root 플래그만 사용하여 모든 의존성(pandas 포함)을 설치합니다.
RUN poetry install --no-root

# 2단계: 최종 실행 환경 (최소한의 런타임 이미지)
FROM python:3.13-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1
ENV PATH="/app/.venv/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# 런타임에 필요한 시스템 라이브러리 복사
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 빌더 단계에서 설치된 의존성을 복사
COPY --from=builder /app/.venv /app/.venv

# 모든 소스 코드를 복사 (프로젝트 루트 디렉토리의 모든 파일/폴더)
COPY . /app

# run.sh를 위해 scripts 폴더 복사 및 실행 권한 부여
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh

# 8000번 포트 노출
EXPOSE 8000

# run.sh를 통해 애플리케이션 실행
CMD ["/scripts/run.sh"]