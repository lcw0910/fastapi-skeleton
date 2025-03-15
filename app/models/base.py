from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from typing import Optional

from app.db.session import Base


class BaseModel(Base):
    """
    모든 모델의 기본이 되는 추상 기본 클래스
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        클래스 이름을 소문자로 변환하여 테이블 이름으로 사용
        """
        return cls.__name__.lower()
