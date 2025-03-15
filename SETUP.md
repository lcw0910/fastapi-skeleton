# 프로젝트 설정 및 실행 방법

## 1. 프로젝트 구조

이 프로젝트는 FastAPI, PostgreSQL, Redis, RabbitMQ를 사용하는 Python 기반 백엔드 애플리케이션입니다.

```
.
├── app/                        # 애플리케이션 패키지
│   ├── api/                    # API 엔드포인트
│   │   └── v1/                 # API 버전 1
│   │       ├── endpoints/      # 개별 엔드포인트 모듈
│   │       └── router.py       # API 라우터
│   ├── core/                   # 핵심 설정 및 유틸리티
│   │   └── config.py           # 애플리케이션 설정
│   ├── db/                     # 데이터베이스 관련 모듈
│   │   └── session.py          # 데이터베이스 세션 관리
│   ├── models/                 # 데이터베이스 모델
│   │   └── base.py             # 기본 모델 클래스
│   ├── schemas/                # Pydantic 스키마
│   ├── services/               # 서비스 모듈
│   │   ├── redis_service.py    # Redis 서비스
│   │   └── rabbitmq_service.py # RabbitMQ 서비스
│   └── main.py                 # 애플리케이션 진입점
├── migrations/                 # Alembic 마이그레이션
├── tests/                      # 테스트 디렉토리
├── .env                        # 환경 변수 파일
├── alembic.ini                 # Alembic 설정 파일
├── docker-compose.yml          # Docker Compose 설정
└── requirements.txt            # 의존성 목록
```

## 2. 환경 설정

### 사전 요구사항
- Python 3.12+
- Docker 및 Docker Compose

### 가상환경 설정

```bash
# 가상환경 생성
python3.12 -m venv venv

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 3. 도커 컨테이너 실행

```bash
# 도커 컨테이너 실행 (PostgreSQL, Redis, RabbitMQ)
docker compose up -d
```

## 4. 데이터베이스 마이그레이션

```bash
# 마이그레이션 실행
alembic upgrade head
```

## 5. 애플리케이션 실행

### 명령행에서 실행
```bash
# 개발 모드로 실행
python -m app.main
```

### Cursor IDE에서 실행
1. F5 키를 누르고 "Python: FastAPI (디버그)" 또는 "Python: FastAPI (일반 실행)" 선택
2. 또는 `Ctrl+Shift+P` (Mac에서는 `Cmd+Shift+P`)를 누르고 "Tasks: Run Task" > "실행: FastAPI" 선택

## 6. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 7. 서비스 상태 확인
- 애플리케이션 상태: http://localhost:8000/health
- 데이터베이스 상태: http://localhost:8000/api/v1/health/db
- Redis 상태: http://localhost:8000/api/v1/health/redis
- RabbitMQ 상태: http://localhost:8000/api/v1/health/rabbitmq 