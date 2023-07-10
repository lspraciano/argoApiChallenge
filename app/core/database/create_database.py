import platform

from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.sql import text

from configuration.configs import settings


async def create_database():
    database_full_url: str = settings.DB_URL
    database_name: str = database_full_url.split('/')[-1]
    create_url: str = database_full_url.replace(f"/{database_name}", "")

    engine_async: AsyncEngine = create_async_engine(
        url=create_url,
        isolation_level="AUTOCOMMIT"
    )

    try:
        async with engine_async.connect() as conn:
            await conn.execute(text(f'CREATE DATABASE "{database_name}"'))
            print('Database Created Successfully')
    except ProgrammingError:
        print('Database Detected')

    del engine_async
    del database_full_url
    del database_name
    del create_url


if __name__ == "__main__":
    import asyncio

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_database())
