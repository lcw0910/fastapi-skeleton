from fastapi import APIRouter

# 개별 라우터 가져오기
from app.api.v1.endpoints import health
# from app.api.v1.endpoints import items, users

api_router = APIRouter()

# 개별 라우터 등록
api_router.include_router(health.router, prefix="/health", tags=["health"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"]) 