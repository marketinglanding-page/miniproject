#!/bin/sh
set -e # 명령어 중 하나라도 실패하면 스크립트 즉시 종료

# ----------------------------------------------
# 1. DB 연결 준비 확인
# ----------------------------------------------
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started successfully."

# ----------------------------------------------
# 2. Django 마이그레이션 자동 수행
# ----------------------------------------------
# 운영/배포 환경에서 컨테이너 실행 시 makemigrations를 수행할 필요는 없습니다.
# (로컬에서 이미 생성/관리되었기 때문) 오직 migrate만 수행합니다.
echo "Running database migrations..."
python manage.py migrate --noinput

# ----------------------------------------------
# 3. Gunicorn 서버 실행
# ----------------------------------------------
echo "Starting Gunicorn server..."
# --workers: 워커 수는 보통 2 * CPU 코어 수 + 1 로 설정
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-level info