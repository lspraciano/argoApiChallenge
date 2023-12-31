from fastapi import FastAPI

from app.api.api import api_factory

app: FastAPI = api_factory()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info",
        reload=True
    )
