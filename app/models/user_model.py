from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database.database import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    password_reset_cod: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    last_change_owner: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
