from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import TokenPayload

# 토큰 URL 경로 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    현재 인증된 사용자 가져오기
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증에 실패했습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 토큰 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=int(user_id), exp=payload.get("exp"))
    except JWTError:
        raise credentials_exception

    # 사용자 조회
    result = await db.execute(select(User).filter(User.id == token_data.sub))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    현재 활성 사용자 가져오기
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다",
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    현재 슈퍼유저 가져오기
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 충분하지 않습니다",
        )
    return current_user
