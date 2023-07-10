import platform
import sys

from app.core.database.create_admin_user import create_user_admin
from app.core.database.create_database import create_database
from app.core.database.create_tables import create_tables
from configuration.configs import settings


async def init_db() -> None:
    if (
            (
                    "pytest" in sys.modules
                    and
                    settings.APP_RUNNING_MODE != "testing"
            )
            or
            (
                    "pytest" not in sys.modules
                    and
                    settings.APP_RUNNING_MODE == "testing"
            )

    ):
        raise Exception(
            "The application cannot be started. Check ARGOAPI_APP_RUNNING_MODE"
        )

    await create_database()

    await create_tables(
        drop_all=settings.APP_RUNNING_MODE == "testing"
    )
    await create_user_admin()


if __name__ == "__main__":
    import asyncio

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(init_db())
