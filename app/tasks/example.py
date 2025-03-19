from app.core.celery import celery
import time
from celery import shared_task
from celery.result import AsyncResult
from celery.states import PENDING, STARTED, SUCCESS, FAILURE, RETRY


@celery.task
def add(x: int, y: int) -> int:
    return x + y


@celery.task
def multiply(x: int, y: int) -> int:
    return x * y


@shared_task(bind=True)
def long_running_task(self, seconds: int) -> dict:
    """
    시간이 오래 걸리는 작업을 시뮬레이션하는 태스크
    bind=True 옵션으로 self 인자를 받아 태스크 인스턴스에 접근할 수 있음
    """
    # 초기 상태 업데이트
    self.update_state(state=STARTED, meta={"progress": 0, "total": seconds})

    # 진행 상황을 단계별로 업데이트
    for i in range(seconds):
        # 1초 대기
        time.sleep(1)

        # 진행 상황 업데이트 (%)
        progress = (i + 1) / seconds * 100
        self.update_state(
            state=STARTED,
            meta={
                "progress": i + 1,
                "total": seconds,
                "percent": progress,
                "status_message": f"작업 진행 중... {progress:.1f}% 완료",
            },
        )

    # 최종 결과 반환
    return {"status": "completed", "process_time": seconds}


def get_task_status(task_id: str) -> dict:
    """
    태스크 ID로 상태를 조회
    """
    task_result = AsyncResult(task_id)

    # 기본 결과 구성
    result = {
        "task_id": task_id,
        "status": task_result.status,
    }

    # 태스크 상태별 처리
    if task_result.status == PENDING:
        # 대기 중인 태스크
        result["status_message"] = "태스크가 대기 중입니다."

    elif task_result.status == STARTED:
        # 실행 중인 태스크
        try:
            # info 속성에서 메타데이터 가져오기 (None일 수 있음)
            if task_result.info is not None and isinstance(task_result.info, dict):
                # 진행 상황 정보 추가
                result.update(
                    {
                        "progress": task_result.info.get("progress", 0),
                        "total": task_result.info.get("total", 1),
                        "percent": task_result.info.get("percent", 0),
                        "status_message": task_result.info.get(
                            "status_message", "실행 중..."
                        ),
                    }
                )
            else:
                # info가 없거나 딕셔너리가 아닌 경우
                result["status_message"] = "작업이 진행 중입니다."
        except Exception as e:
            # 메타데이터 접근 중 오류가 발생하는 경우
            result["status_message"] = f"작업 진행 중 (상세 정보 없음: {str(e)})"

    elif task_result.status == SUCCESS:
        # 성공한 태스크
        try:
            # get() 메서드로 결과 가져오기
            task_data = task_result.get()
            result["result"] = task_data
            result["status_message"] = "작업이 완료되었습니다."
        except Exception as e:
            result["status_message"] = (
                f"작업은 완료되었으나 결과를 가져오는 중 오류 발생: {str(e)}"
            )

    elif task_result.status == FAILURE:
        # 실패한 태스크
        result["error"] = (
            str(task_result.result) if task_result.result else "알 수 없는 오류"
        )
        result["status_message"] = "작업이 실패했습니다."

    elif task_result.status == RETRY:
        # 재시도 중인 태스크
        result["status_message"] = "작업을 재시도 중입니다."

    else:
        # 기타 상태 (REVOKED 등)
        result["status_message"] = f"작업 상태: {task_result.status}"

    return result
