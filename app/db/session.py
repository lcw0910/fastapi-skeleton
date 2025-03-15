from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import logging
from typing import AsyncGenerator

from app.core.config import settings

# 로거 설정
logger = logging.getLogger(__name__)


# Base 모델 정의
class Base(DeclarativeBase):
    pass


try:
    # 비동기 엔진 생성
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,  # 연결 유효성 검사
    )

    # 비동기 세션 생성 (SQLAlchemy 2.0 방식)
    AsyncSessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
    )
except Exception as e:
    logger.error(f"데이터베이스 연결 실패: {e}")
    # 애플리케이션이 실행될 수 있도록 더미 엔진과 세션 생성
    engine = None
    AsyncSessionLocal = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    요청마다 새 세션을 생성하고 완료 후 종료하는 의존성 주입 함수
    """
    if AsyncSessionLocal is None:
        logger.error("데이터베이스 세션을 생성할 수 없습니다.")
        raise Exception("데이터베이스 연결이 구성되지 않았습니다.")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
