import pika
import asyncio
from app.core.config import settings

class RabbitMQService:
    def __init__(self):
        """
        RabbitMQ 서비스 클래스 초기화
        """
        self.connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=pika.PlainCredentials(
                username=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD,
            )
        )
        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        """
        RabbitMQ 서버에 연결
        """
        # pika는 비동기를 직접 지원하지 않으므로 런루프에서 실행
        try:
            loop = asyncio.get_running_loop()
            self.connection = await loop.run_in_executor(
                None, lambda: pika.BlockingConnection(self.connection_params)
            )
            self.channel = await loop.run_in_executor(
                None, lambda: self.connection.channel()
            )
        except Exception as e:
            print(f"RabbitMQ 연결 실패: {e}")
            self.connection = None
            self.channel = None
            raise

    async def check_connection(self) -> bool:
        """
        RabbitMQ 연결 상태 확인
        """
        try:
            if self.connection is None:
                await self.connect()
            return self.connection is not None and self.connection.is_open
        except Exception:
            return False

    async def publish_message(self, exchange: str, routing_key: str, message: str) -> bool:
        """
        메시지 발행
        """
        if not await self.check_connection():
            await self.connect()
        
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # 메시지 지속성 설정
                    )
                )
            )
            return True
        except Exception as e:
            print(f"메시지 발행 실패: {e}")
            return False

    async def close(self) -> None:
        """
        RabbitMQ 연결 종료
        """
        if self.connection and self.connection.is_open:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: self.connection.close()) 