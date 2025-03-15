from datetime import datetime
from typing import Optional, List, Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, or_

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    ID로 사용자 조회
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    이메일로 사용자 조회
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    사용자명으로 사용자 조회
    """
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    """
    모든 사용자 조회
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    사용자 생성
    """
    # 해싱된 비밀번호로 새 User 객체 생성
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    db: AsyncSession, user_id: int, user_in: UserUpdate
) -> Optional[User]:
    """
    사용자 정보 업데이트
    """
    # 업데이트할 데이터 준비
    update_data = user_in.model_dump(exclude_unset=True)

    # 비밀번호가 제공된 경우 해시 처리
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    # 업데이트 수행
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        query = update(User).where(User.id == user_id).values(**update_data)
        await db.execute(query)
        await db.commit()

    return await get_user_by_id(db, user_id)


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    사용자 삭제
    """
    query = delete(User).where(User.id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


async def authenticate_user(
    db: AsyncSession, username_or_email: str, password: str
) -> Optional[User]:
    """
    사용자 인증
    """
    # 이메일 또는 사용자명으로 조회
    result = await db.execute(
        select(User).filter(
            or_(User.email == username_or_email, User.username == username_or_email)
        )
    )
    user = result.scalars().first()

    # 사용자가 존재하고 비밀번호가 일치하는지 확인
    if not user or not verify_password(password, user.hashed_password):
        return None

    # 마지막 로그인 시간 업데이트
    user.last_login = datetime.utcnow()
    await db.commit()

    return user
