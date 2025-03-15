#!/usr/bin/env python
"""
개발 환경에서 애플리케이션을 실행하기 위한 스크립트입니다.
reload 옵션이 항상 활성화되어 있어 코드 변경 시 자동으로 서버가 재시작됩니다.
수정 테스트
"""

import os
import uvicorn
from dotenv import load_dot

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    # 환경 변수 설정 (만약 .env 파일에 없다면)
    os.environ.setdefault("DEBUG", "True")

    # 포트 충돌 해결을 위한 대체 포트
    default_port = 8000
    try:
        uvicorn.run(
            "app.main:app",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", default_port)),
            reload=True,  # 항상 리로드 활성화
            workers=1,  # 개발 환경에서는 단일 워커 사용
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print(
                f"포트 {default_port}가 이미 사용 중입니다. 대체 포트 {default_port+1}로 시도합니다."
            )
            # 포트 충돌 시 다음 포트 시도
            uvicorn.run(
                "app.main:app",
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", default_port + 1)),
                reload=True,
                workers=1,
            )
        else:
            # 다른 오류 발생 시 그대로 출력
            raise
