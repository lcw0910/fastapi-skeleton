import os
from typing import List, Union
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = Field(default=os.getenv("APP_NAME", "fastapi-app"))
    PROJECT_NAME: str = Field(default=os.getenv("PROJECT_NAME", "FastAPI 애플리케이션"))
    APP_ENV: str = Field(default=os.getenv("APP_ENV", "development"))
    DEBUG: bool = Field(default=os.getenv("DEBUG", "False").lower() == "true")
    SECRET_KEY: str = Field(
        default=os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    )

    # API 설정
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = []

    # 데이터베이스 설정
    DB_HOST: str = Field(default=os.getenv("DB_HOST", "localhost"))
    DB_PORT: int = Field(default=int(os.getenv("DB_PORT", "5432")))
    DB_USER: str = Field(default=os.getenv("DB_USER", "postgres"))
    DB_PASSWORD: str = Field(default=os.getenv("DB_PASSWORD", "postgres"))
    DB_NAME: str = Field(default=os.getenv("DB_NAME", "app"))
    DATABASE_URL: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        )
    )

    # Redis 설정
    REDIS_HOST: str = Field(default=os.getenv("REDIS_HOST", "localhost"))
    REDIS_PORT: int = Field(default=int(os.getenv("REDIS_PORT", "6379")))
    REDIS_PASSWORD: str = Field(default=os.getenv("REDIS_PASSWORD", ""))
    REDIS_DB: int = Field(default=int(os.getenv("REDIS_DB", "0")))

    # RabbitMQ 설정
    RABBITMQ_HOST: str = Field(default=os.getenv("RABBITMQ_HOST", "localhost"))
    RABBITMQ_PORT: int = Field(default=int(os.getenv("RABBITMQ_PORT", "5672")))
    RABBITMQ_USER: str = Field(default=os.getenv("RABBITMQ_USER", "rabbit"))
    RABBITMQ_PASSWORD: str = Field(default=os.getenv("RABBITMQ_PASSWORD", "rabbit"))
    RABBITMQ_VHOST: str = Field(default=os.getenv("RABBITMQ_VHOST", "/"))

    # 서버 설정
    HOST: str = Field(default=os.getenv("HOST", "0.0.0.0"))
    PORT: int = Field(default=int(os.getenv("PORT", "8000")))

    # CORS 설정 후처리
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "")
        if cors_origins:
            origins = [origin.strip() for origin in cors_origins.split(",")]
            self.BACKEND_CORS_ORIGINS = origins


settings = Settings()
