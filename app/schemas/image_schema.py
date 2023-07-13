from typing import Optional, Annotated

from fastapi import Query, Path
from fastapi import UploadFile, File
from pydantic import BaseModel

from app.schemas.user_schema import UserSchemaBasic


class ImageSchemaBasic(BaseModel):
    id: int
    name: str
    approved_by: Optional[int] = None
    approved: Optional[int] = None
    status: int
    approved_by_rl: Optional[UserSchemaBasic] = None

    class Config:
        orm_mode = True


class ImageByIdQueryParamsSchema(BaseModel):
    name: Optional[str] = Query(None, description="Nome do arquivo")
    approved_by: Optional[int] = Query(None, description="ID do usuário que aprovou")
    approved: Optional[int] = Query(None, description="0 - Não Aprovado | 1 - Aprovado")


class ImagePostSchema(BaseModel):
    image: UploadFile = File(...)


class ImageApprovalSchema(BaseModel):
    images_ids_list: list[int]
    approval_result: int


class ImageResponse(BaseModel):
    file_data: bytes


ImageIdSchema = Annotated[
    int,
    Path(
        title="Image ID",
        description="The ID of the Image",
        ge=1
    )
]
