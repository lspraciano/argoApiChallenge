from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchemaBasic(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: int

    class Config:
        orm_mode = True


class UserSchemaCreateRequest(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSchemaCreateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSchemaUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[int] = None


class UserSchemaUpdatePassword(BaseModel):
    new_password: str
