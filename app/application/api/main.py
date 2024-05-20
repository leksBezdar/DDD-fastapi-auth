from fastapi import FastAPI

from application.api.users.routers import group_router
from .healthcheck import healthcheck_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD auth",
        description="IP address? How do they know where i pee?",
        debug=False,
    )

    app.include_router(group_router, prefix="/groups", tags=["GROUP"])
    app.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])

    return app
