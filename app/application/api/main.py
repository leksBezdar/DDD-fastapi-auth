from contextlib import asynccontextmanager
from fastapi import FastAPI

from application.api.lifespan import close_kafka, start_kafka
from application.api.users.routers import group_router, user_router
from .healthcheck import healthcheck_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await close_kafka()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD auth",
        description="IP address? How do they know where i pee?",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(group_router, prefix="/groups", tags=["GROUP"])
    app.include_router(user_router, prefix="/users", tags=["USER"])

    app.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])

    return app
