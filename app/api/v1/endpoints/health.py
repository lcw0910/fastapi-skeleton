from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db
from app.services.redis_service import RedisService
from app.services.rabbitmq_service import RabbitMQService


router = APIRouter()


@router.get("/")
async def health_check():
    """
    애플리케이션 상태 확인용 엔드포인트
    """
    return {"status": "healthy"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    데이터베이스 연결 상태 확인용 엔드포인트
    """
    try:
        # 간단한 쿼리 실행
        await db.execute(text("SELECT 1"))
        return {"status": "database connected"}
    except Exception as e:
        return {"status": "database error", "detail": str(e)}


@router.get("/redis")
async def redis_health_check():
    """
    Redis 연결 상태 확인용 엔드포인트
    """
    try:
        redis_service = RedisService()
        await redis_service.ping()
        return {"status": "redis connected"}
    except Exception as e:
        return {"status": "redis error", "detail": str(e)}


@router.get("/rabbitmq")
async def rabbitmq_health_check():
    """
    RabbitMQ 연결 상태 확인용 엔드포인트
    """
    try:
        rabbitmq_service = RabbitMQService()
        is_connected = await rabbitmq_service.check_connection()
        if is_connected:
            return {"status": "rabbitmq connected"}
        else:
            return {"status": "rabbitmq not connected"}
    except Exception as e:
        return {"status": "rabbitmq error", "detail": str(e)}
