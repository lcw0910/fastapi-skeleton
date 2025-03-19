from celery import Celery
import os

# 환경 변수로 설정된 브로커와 백엔드 URL을 가져오거나 기본값 사용
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

# Redis URL 구성
redis_url = f"redis://{REDIS_HOST}:6379/0"

celery = Celery(
    "app",
    broker=f"amqp://rabbit:rabbit@{RABBITMQ_HOST}:5672//",
    backend=redis_url,
    include=["app.tasks"],
)

celery.conf.update(
    # 직렬화 설정
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    # 시간대 설정
    timezone="Asia/Seoul",
    enable_utc=True,
    # 태스크 상태 및 결과 관련 설정
    task_track_started=True,  # 태스크가 시작될 때 상태를 STARTED로 설정
    task_ignore_result=False,  # 태스크 결과 저장
    result_expires=3600,  # 결과는 1시간 동안 유지
    # 이벤트 관련 설정 (상태 모니터링에 중요)
    worker_send_task_events=True,  # 워커가 태스크 이벤트를 전송
    task_send_sent_event=True,  # 태스크 전송 이벤트도 전송
    # 결과 백엔드 명시적 설정
    result_backend=redis_url,
)
