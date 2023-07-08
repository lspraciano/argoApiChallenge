import platform

from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.core.database.database import async_session
from app.core.security.password_manager import generate_hash_password
from app.models.user_model import UserModel
from configuration.configs import settings


async def create_user_admin() -> None:
    async with async_session() as session:
        query: Select = select(UserModel).filter(
            UserModel.name == settings.ADMIN_USER_NAME
        )
        result: Result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

    if not user:
        print("Creating Admin User")

        user: UserModel = UserModel(
            name=settings.ADMIN_USER_NAME,
            email=settings.ADMIN_USER_EMAIL,
            password=generate_hash_password(
                settings.ADMIN_PASSWORD
            )
        )

        async with async_session() as session:
            session.add(user)
            await session.commit()


if __name__ == "__main__":
    import asyncio

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_user_admin())
