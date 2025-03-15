import asyncio
import sys
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_user_by_email


async def create_first_superuser():
    print("초기 슈퍼유저 생성을 시작합니다...")

    # 데이터베이스 연결 설정
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        # 이미 존재하는지 확인
        existing_admin = await get_user_by_email(db, "admin@example.com")
        if existing_admin:
            print("슈퍼유저가 이미 존재합니다.")
            return

        # 슈퍼유저 정보 생성
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            password="adminpassword",  # 실제 환경에서는 더 강력한 비밀번호를 사용하세요
            is_active=True,
            is_superuser=True,
        )

        # 사용자 생성
        user = await create_user(db, user_in=user_in)
        print(f"슈퍼유저가 생성되었습니다: ID {user.id}, 이메일 {user.email}")

    await engine.dispose()
    print("완료!")


if __name__ == "__main__":
    asyncio.run(create_first_superuser())
