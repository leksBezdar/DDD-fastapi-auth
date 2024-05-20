from fastapi import APIRouter


user_router = APIRouter()


@user_router.post("/")
async def hello_world():
    return {"Message": "Hello, World!"}
