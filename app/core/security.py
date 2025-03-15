from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 비밀번호 해싱에 사용할 알고리즘 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 관련 설정
# 환경 변수에서 이것들을 설정하도록 core/config.py에 추가해야 합니다
SECRET_KEY = getattr(
    settings, "SECRET_KEY", "your-secret-key-here-change-in-production"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    일반 텍스트 비밀번호와 해시된 비밀번호 비교
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해싱
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    JWT 액세스 토큰 생성
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
