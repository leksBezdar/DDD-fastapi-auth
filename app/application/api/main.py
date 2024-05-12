from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(
        title="DDD auth",
        description="IP address? How do they know where i pee?",
        debug=True,
    )
