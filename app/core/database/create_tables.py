import platform

from app.core.database.database import engine_async, ModelBase


async def create_tables(
        drop_all: bool = False
) -> None:
    async with engine_async.begin() as conn:
        if drop_all:
            print("Creating Tables")
            await conn.run_sync(
                ModelBase.metadata.drop_all
            )

        await conn.run_sync(
            ModelBase.metadata.create_all
        )
    await engine_async.dispose()


if __name__ == "__main__":
    import asyncio

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_tables())
