from pydantic import BaseModel, EmailStr


class UserSchemaBasic(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: int

    class Config:
        orm_mode = True
