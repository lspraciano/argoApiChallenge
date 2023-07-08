from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


@declarative_mixin
class CommonFields:
    @declared_attr
    def last_change_owner(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    @declared_attr
    def last_change(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
