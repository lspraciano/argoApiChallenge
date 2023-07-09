from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database.database import ModelBase
from app.schemas.user_schema import UserSchemaBasic


class CommentModel(ModelBase):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id"), nullable=False)
    owner: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    creation_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                         server_default=func.now())
    status = mapped_column(Integer, nullable=False, server_default="1")

    owner_rl: Mapped[UserSchemaBasic] = relationship(
        "UserModel",
        foreign_keys=[owner],
        lazy="joined"
    )
