#!/bin/bash

# 스크립트의 디렉토리 경로를 구합니다
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# 가상환경 활성화
source "${PROJECT_ROOT}/venv/bin/activate"

# Redis 연결 확인
echo "Redis 연결 확인 중..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "경고: Redis 서버에 연결할 수 없습니다. docker-compose로 Redis가 실행 중인지 확인하세요."
    echo "Redis 없이 계속 진행하면 태스크 상태 및 결과가 저장되지 않을 수 있습니다."
    read -p "계속 진행하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Celery worker 실행을 취소합니다."
        exit 1
    fi
else
    echo "Redis 서버가 실행 중입니다."
fi

# Celery worker 실행 (디버깅 모드)
echo "Celery worker 시작 중..."
celery -A app.core.celery worker \
    --loglevel=info \
    --concurrency=1 \
    --events \
    -E 