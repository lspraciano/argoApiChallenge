from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import api_router
from app.core.database.init_db import init_db
from configuration.configs import settings


def api_factory() -> FastAPI:
    origins: list = ["*"]

    current_api: FastAPI = FastAPI(
        title="Argo Challenge - API",
        description="API for the Argo Challenge",
        version="1.0",
        contact={
            "name": "Lucas Praciano",
            "email": "lspraciano@gmail.com",
        },
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "operationsSorter": "method",
            "filter": True,
            "docExpansion": None
        },
    )

    current_api.include_router(
        api_router,
        prefix=settings.API_URL
    )

    current_api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    current_api: FastAPI = register_events(
        api=current_api
    )

    return current_api


def register_events(
        api: FastAPI
) -> FastAPI:
    @api.on_event("startup")
    async def startup():
        print(f"Running Mode: {settings.APP_RUNNING_MODE}")
        await init_db()

    @api.on_event("shutdown")
    async def shutdown():
        ...

    return api
