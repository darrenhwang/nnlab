from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from mock_service import MockService
from mock_schemas import EvaluationRequest, Model

# 创建路由器
evaluation_router = APIRouter()
evaluation_service = MockService()

@evaluation_router.post("/evaluate/{model_id}")
async def evaluate_model(
    model_id: str,
    request: EvaluationRequest
) -> Dict[str, Any]:
    """评估模型性能"""
    try:
        # 获取模型信息
        model = Model.get(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # 评估模型
        result = evaluation_service.evaluate_model(
            model=model,
            model_path=request.model_path,
            dataset=request.dataset,
            batch_size=request.batch_size
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建简单路由器
simple_router = APIRouter()

@simple_router.get("/hello")
async def hello():
    """返回问候信息"""
    return {"greeting": "Hello from simple controller"}

@simple_router.get("/echo/{message}")
async def echo(message: str):
    """返回用户输入的消息"""
    return {"message": message, "source": "simple controller"} 