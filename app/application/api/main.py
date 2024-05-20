from fastapi import FastAPI

from application.api.users.handlers import user_router
from .healthcheck import healthcheck_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD auth",
        description="IP address? How do they know where i pee?",
        debug=True,
    )

    app.include_router(user_router, prefix="/users", tags=["USER"])
    app.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])

    return app
