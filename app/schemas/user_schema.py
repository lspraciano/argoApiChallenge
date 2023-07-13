from typing import Optional, Annotated

from fastapi import Path
from pydantic import BaseModel, EmailStr


class UserSchemaBasic(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: int

    class Config:
        orm_mode = True


class UserSchemaCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSchemaUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True


class UserSchemaUpdatePassword(BaseModel):
    new_password: str

    class Config:
        orm_mode = True


class UserAuthentication(BaseModel):
    access_token: str
    token_type: str
    user_email: str
    user_id: str

    class Config:
        orm_mode = True


UserIdSchema = Annotated[
    int,
    Path(
        title="User ID",
        description="The ID of the User",
        ge=1
    )
]
