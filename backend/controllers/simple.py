from fastapi import APIRouter

router = APIRouter()

@router.get("/echo/{message}")
async def echo(message: str):
    """返回用户输入的消息"""
    return {"message": message, "source": "simple controller"}

@router.get("/hello")
async def hello():
    """返回问候信息"""
    return {"greeting": "Hello from simple controller"} 