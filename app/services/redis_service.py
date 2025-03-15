import redis.asyncio as redis
from app.core.config import settings

class RedisService:
    def __init__(self):
        """
        Redis 서비스 클래스 초기화
        """
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            db=settings.REDIS_DB,
            decode_responses=True,
        )
    
    async def ping(self) -> bool:
        """
        Redis 서버 연결 상태 확인
        """
        return await self.redis_client.ping()
    
    async def get(self, key: str) -> str:
        """
        키에 해당하는 값 조회
        """
        return await self.redis_client.get(key)
    
    async def set(self, key: str, value: str, expire: int = None) -> bool:
        """
        키-값 저장, 선택적으로 만료 시간 설정
        """
        if expire:
            return await self.redis_client.setex(key, expire, value)
        return await self.redis_client.set(key, value)
    
    async def delete(self, key: str) -> int:
        """
        키 삭제
        """
        return await self.redis_client.delete(key)
    
    async def close(self) -> None:
        """
        Redis 연결 종료
        """
        await self.redis_client.close() 