#!/bin/bash

# 스크립트의 디렉토리 경로를 구합니다
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# 가상환경 활성화
source "${PROJECT_ROOT}/venv/bin/activate"

# 서비스 연결 확인
echo "서비스 연결 확인 중..."

# Redis 연결 확인
if ! redis-cli ping > /dev/null 2>&1; then
    echo "경고: Redis 서버에 연결할 수 없습니다. docker-compose로 Redis가 실행 중인지 확인하세요."
else
    echo "Redis 서버가 실행 중입니다."
fi

# RabbitMQ 연결 확인 (간단한 방법)
if ! curl -s -u rabbit:rabbit http://localhost:15672/api/overview > /dev/null 2>&1; then
    echo "경고: RabbitMQ 서버에 연결할 수 없습니다. docker-compose로 RabbitMQ가 실행 중인지 확인하세요."
else
    echo "RabbitMQ 서버가 실행 중입니다."
fi

# Celery 워커 프로세스 확인
if ! pgrep -f "celery.*worker" > /dev/null; then
    echo "경고: Celery worker가 실행 중이지 않습니다. 먼저 worker를 실행해야 합니다."
    echo "worker 실행 방법: ./scripts/run_celery.sh"
fi

# Flower 실행
echo "Flower 시작 중..."
celery -A app.core.celery flower \
    --port=5555 \
    --persistent=True \
    --broker_api=http://rabbit:rabbit@localhost:15672/api/ 