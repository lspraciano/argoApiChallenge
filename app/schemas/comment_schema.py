from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import UserSchemaBasic


class CommentSchemaBasic(BaseModel):
    id: int
    content: str
    image_id: int
    owner: int
    creation_date_time: datetime
    status: int
    owner_rl: Optional[UserSchemaBasic]

    class Config:
        orm_mode = True


class CommentCreateSchema(BaseModel):
    content: str
    image_id: int


class CommentUpdateSchema(BaseModel):
    content: Optional[str] = None
    status: Optional[int] = None
