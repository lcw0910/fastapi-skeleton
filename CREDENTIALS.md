# 계정 정보 문서

이 문서에는 애플리케이션 접속을 위한 초기 계정 정보가 포함되어 있습니다.

## 개발 환경 계정

### 슈퍼유저 계정
- **이메일**: admin@example.com
- **사용자명**: admin
- **비밀번호**: adminpassword
- **권한**: 슈퍼유저(관리자)

> **주의**: 이 계정은 개발 및 테스트 목적으로만 사용해야 합니다. 프로덕션 환경에서는 강력한 비밀번호를 사용하여 새 관리자 계정을 생성하세요.

## 서비스 접속 정보

### RabbitMQ 관리자 UI
- **URL**: http://localhost:15672
- **사용자명**: rabbit
- **비밀번호**: rabbit
- **포트**: 
  - 관리자 UI: 15672
  - AMQP: 5672

### Flower (Celery 모니터링)
- **URL**: http://localhost:5555
- **포트**: 5555

## 계정 생성 방법

추가 계정이 필요한 경우 다음과 같은 방법으로 생성할 수 있습니다:

### API를 통한 생성
슈퍼유저 계정으로 로그인한 후, 다음 API 엔드포인트를 사용하여 새 사용자를 생성할 수 있습니다:
```
POST /api/v1/users/
```

요청 데이터 예시:
```json
{
  "email": "user@example.com",
  "username": "user",
  "password": "userpassword",
  "is_active": true,
  "is_superuser": false
}
```

### 직접 스크립트 실행

`create_superuser.py` 스크립트를 수정하여 새 슈퍼유저를 생성할 수도 있습니다:

```bash
python create_superuser.py
```

## API 인증

API 호출 시 다음과 같이 토큰 인증을 사용해야 합니다:

1. 로그인 API 호출:
```
POST /api/v1/auth/login
```

2. 반환된 토큰을 사용하여 Authorization 헤더 설정:
```
Authorization: Bearer {액세스 토큰}
```

## 비밀번호 변경

계정의 비밀번호를 변경하려면 다음 API를 사용하세요:
```
PUT /api/v1/users/me
```

요청 데이터 예시:
```json
{
  "password": "새로운비밀번호"
}
``` 