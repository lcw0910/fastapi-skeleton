# FastAPI 애플리케이션 스켈레톤

Python 3.12 기반의 FastAPI 애플리케이션 스켈레톤 프로젝트입니다. PostgreSQL, Redis, RabbitMQ를 포함하고 있습니다.

## 기술 스택

- Python 3.12+
- FastAPI
- SQLAlchemy (비동기)
- Alembic
- PostgreSQL
- Redis
- RabbitMQ
- Docker & Docker Compose

## 시작하기

### 필수 조건

- Python 3.12 이상
- Docker 및 Docker Compose

### 설치 방법

1. 저장소 클론

```bash
git clone <repository-url>
cd python-skeleton
```

2. 가상환경 생성 및 활성화

```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. Docker 컨테이너 실행

```bash
docker-compose up -d
```

5. 데이터베이스 마이그레이션 실행

```bash
alembic upgrade head
```

6. 기본 슈퍼유저 생성

```bash
python create_superuser.py
```

7. 애플리케이션 실행

다음 방법 중 하나를 선택하여 애플리케이션을 실행할 수 있습니다:

```bash
# 방법 1: 기본 실행 (reload 옵션 활성화)
python -m app.main

# 방법 2: 개발 스크립트 사용 (포트 충돌 자동 해결 기능 포함)
python run_dev.py

# 방법 3: uvicorn 직접 실행
uvicorn app.main:app --reload
```

### 계정 정보

개발 및 테스트를 위한 초기 슈퍼유저 계정 정보는 [CREDENTIALS.md](CREDENTIALS.md) 파일에서 확인할 수 있습니다.

## 프로젝트 구조

```
.
├── alembic.ini                  # Alembic 설정 파일
├── app                          # 애플리케이션 패키지
│   ├── api                      # API 엔드포인트
│   │   └── v1                   # API 버전 1
│   │       ├── endpoints        # 개별 엔드포인트 모듈
│   │       └── router.py        # API 라우터
│   ├── core                     # 핵심 설정 및 유틸리티
│   │   └── config.py            # 애플리케이션 설정
│   ├── db                       # 데이터베이스 관련 모듈
│   │   └── session.py           # 데이터베이스 세션 관리
│   ├── models                   # 데이터베이스 모델
│   │   └── base.py              # 기본 모델 클래스
│   ├── schemas                  # Pydantic 스키마
│   ├── services                 # 서비스 모듈
│   │   ├── redis_service.py     # Redis 서비스
│   │   └── rabbitmq_service.py  # RabbitMQ 서비스
│   └── main.py                  # 애플리케이션 진입점
├── docker-compose.yml           # Docker Compose 설정
├── migrations                   # Alembic 마이그레이션
├── tests                        # 테스트 디렉토리
├── .env                         # 환경 변수 파일
└── requirements.txt             # 의존성 목록
```

## 환경 변수

`.env` 파일에서 다음 환경 변수를 설정할 수 있습니다:

- `APP_NAME`: 애플리케이션 이름
- `APP_ENV`: 환경 (development, production)
- `DEBUG`: 디버그 모드 활성화 여부
- `SECRET_KEY`: 보안 키
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: 데이터베이스 연결 정보
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`: Redis 연결 정보
- `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST`: RabbitMQ 연결 정보
- `HOST`, `PORT`: 서버 호스트 및 포트

## API 문서

애플리케이션 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 