from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app.api.v1.api import api_router
from app.core.config import settings

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI 기반 백엔드 API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 미들웨어 설정
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    루트 엔드포인트 - API 상태 확인
    """
    return {
        "status": "online",
        "message": f"{settings.PROJECT_NAME} API가 실행 중입니다",
        "version": "0.1.0",
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    # DEBUG 환경 변수가 설정되지 않았거나 "false"인 경우에도 기본적으로 reload=True로 설정
    debug_mode = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=True,  # 항상 리로드 활성화
        workers=1 if debug_mode else 2,  # 개발 환경에서는 단일 워커 사용
    )
