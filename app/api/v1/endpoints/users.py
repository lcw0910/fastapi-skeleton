from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_superuser, get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_id,
    get_users,
    update_user,
    delete_user,
)

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    모든 사용자 목록 조회 (슈퍼유저만 가능)
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    새 사용자 생성 (슈퍼유저만 가능)
    """
    # 이메일 중복 확인
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다",
        )

    # 사용자명 중복 확인
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다",
        )

    user = await create_user(db, user_in=user_in)
    return user


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    새 사용자 가입 (일반 사용자용)
    """
    # 이메일 중복 확인
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다",
        )

    # 사용자명 중복 확인
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다",
        )

    # 일반 사용자 생성이므로 슈퍼유저 권한은 부여하지 않음
    user_in.is_superuser = False
    user = await create_user(db, user_in=user_in)
    return user


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    현재 사용자 정보 조회
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    현재 사용자 정보 업데이트
    """
    if user_in.username is not None:
        # 사용자명 변경시 중복 확인
        user = await get_user_by_username(db, username=user_in.username)
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자명입니다",
            )

    if user_in.email is not None:
        # 이메일 변경시 중복 확인
        user = await get_user_by_email(db, email=user_in.email)
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다",
            )

    # 일반 사용자는 자신의 슈퍼유저 상태를 변경할 수 없음
    if user_in.is_superuser is not None:
        user_in.is_superuser = current_user.is_superuser

    user = await update_user(db, user_id=current_user.id, user_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    ID로 사용자 조회
    """
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )

    # 슈퍼유저가 아니면 자신의 정보만 조회 가능
    if not current_user.is_superuser and user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 충분하지 않습니다",
        )

    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    사용자 정보 업데이트 (슈퍼유저만 가능)
    """
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )

    if user_in.username is not None:
        # 사용자명 변경시 중복 확인
        existing_user = await get_user_by_username(db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자명입니다",
            )

    if user_in.email is not None:
        # 이메일 변경시 중복 확인
        existing_user = await get_user_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다",
            )

    user = await update_user(db, user_id=user_id, user_in=user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> None:
    """
    사용자 삭제 (슈퍼유저만 가능)
    """
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )

    # 슈퍼유저가 자신을 삭제하려는 경우 방지
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 계정은 삭제할 수 없습니다",
        )

    await delete_user(db, user_id=user_id)
