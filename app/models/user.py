from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt
from app.models.base import BaseModel


class User(BaseModel):
    """
    사용자 모델
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        비밀번호를 해싱하는 함수
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify_password(self, password: str) -> bool:
        """
        제공된 비밀번호가 해시된 비밀번호와 일치하는지 확인하는 함수
        """
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())
