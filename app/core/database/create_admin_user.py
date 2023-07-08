import platform
from typing import Optional, List

from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.core.database.database import async_session
from app.core.security.password_manager import generate_hash_password
from app.models.user_model import UserModel
from configuration.configs import settings


async def create_user_admin() -> None:
    user_list: Optional[List[UserModel]] = []

    async with async_session() as session:
        query: Select = select(UserModel).filter(
            UserModel.name == settings.ONE_ADMIN_USER_NAME
        )
        result: Result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            user: UserModel = UserModel(
                name=settings.ONE_ADMIN_USER_NAME,
                email=settings.ONE_ADMIN_USER_EMAIL,
                password=generate_hash_password(
                    settings.ONE_ADMIN_PASSWORD
                )
            )

            user_list.append(user)

        query: Select = select(UserModel).filter(
            UserModel.name == settings.TWO_ADMIN_USER_NAME
        )
        result: Result = await session.execute(query)
        user_2: UserModel = result.scalars().unique().one_or_none()

        if not user_2:
            user_2: UserModel = UserModel(
                name=settings.TWO_ADMIN_USER_NAME,
                email=settings.TWO_ADMIN_USER_EMAIL,
                password=generate_hash_password(
                    settings.TWO_ADMIN_PASSWORD
                )
            )
            user_list.append(user_2)

        if user_list:
            for user in user_list:
                session.add(user)
            await session.commit()


if __name__ == "__main__":
    import asyncio

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_user_admin())
