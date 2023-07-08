from typing import Optional, List

from pydantic.networks import EmailStr
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.core.database.database import async_session
from app.core.security.password_manager import check_password, generate_hash_password
from app.models.user_model import UserModel


async def get_user_by_id(
        user_id: int
) -> Optional[UserModel]:
    async with async_session() as session:
        query: Select = select(UserModel).where(
            UserModel.id == user_id
        )
        result: Result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

    return user


async def get_all_users() -> Optional[List[UserModel]]:
    async with async_session() as session:
        query: Select = select(UserModel)
        result: Result = await session.execute(query)
        users: Optional[List[UserModel]] = list(result.scalars().unique().all())
    return users


async def authenticate_user(
        email: EmailStr,
        password: str,
) -> Optional[UserModel]:
    async with async_session() as session:
        query: Select = select(UserModel).where(UserModel.email == email)
        result: Result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not check_password(password, user.password):
            return None

        return user


async def create_user(
        name: str,
        email: EmailStr,
        password: str,
        last_change_owner: int
) -> UserModel:
    user: UserModel = UserModel(
        name=name,
        email=email,
        password=generate_hash_password(password),
        status=1,
        last_change_owner=last_change_owner
    )

    async with async_session() as session:
        session.add(user)
        await session.commit()
        return user


async def update_user_by_id(
        user_id: int,
        name: Optional[str] = None,
        email: Optional[EmailStr] = None,
        password: Optional[str] = None,
        status: Optional[int] = None,
        last_change_owner: Optional[int] = None
) -> Optional[UserModel]:
    to_update: UserModel = await get_user_by_id(user_id)

    if not to_update:
        return None

    if name is not None:
        to_update.name = name

    if email is not None:
        to_update.email = email

    if password is not None:
        to_update.password = generate_hash_password(
            password
        )

    if status is not None:
        to_update.status = status

    if last_change_owner is not None:
        to_update.last_change_owner = last_change_owner

    async with async_session() as session:
        session.add(to_update)
        await session.commit()
        return to_update
