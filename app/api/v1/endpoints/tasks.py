from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.tasks.example import long_running_task, get_task_status

router = APIRouter()


class TaskRequest(BaseModel):
    seconds: int = Field(..., ge=1, le=300, description="작업이 실행될 시간(초)")


class TaskResponse(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None
    total: Optional[int] = None
    percent: Optional[float] = None
    status_message: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None


@router.post("/", response_model=TaskResponse)
async def create_task(task_request: TaskRequest):
    """
    비동기 태스크를 실행하고 태스크 ID를 반환합니다.
    """
    task = long_running_task.delay(task_request.seconds)
    return {"task_id": task.id}


@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str):
    """
    태스크 ID로 작업 상태를 조회합니다.
    """
    task_result = get_task_status(task_id)
    return task_result
