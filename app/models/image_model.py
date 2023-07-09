from sqlalchemy import Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database.database import ModelBase
from app.schemas.user_schema import UserSchemaBasic


class ImageModel(ModelBase):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[str] = mapped_column(LargeBinary(length=2048), nullable=False)
    approved_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    approved: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    status: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")

    approved_by_rl: Mapped[UserSchemaBasic] = relationship(
        "UserModel",
        foreign_keys=[approved_by],
        lazy="joined"
    )
