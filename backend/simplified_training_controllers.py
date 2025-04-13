from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from pydantic import BaseModel
from typing import Literal
import asyncio
import uuid

# 导入模拟训练服务
from mock_training import mock_training_service, evaluate_model

# 定义训练配置模型
class TrainingConfig(BaseModel):
    model_id: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int = 64
    epochs: int = 5
    learning_rate: float = 0.001

# 定义评估请求模型
class EvaluationRequest(BaseModel):
    model_path: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int = 64

# 创建路由器
router = APIRouter()

# 存储模型信息
models_db = {}

@router.post("/models")
async def create_model(name: str):
    """创建新模型"""
    model_id = str(uuid.uuid4())
    models_db[model_id] = {
        "id": model_id,
        "name": name,
        "status": "created"
    }
    return {"id": model_id, "name": name, "status": "created"}

@router.get("/models")
async def list_models():
    """列出所有模型"""
    return list(models_db.values())

@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """获取模型信息"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    return models_db[model_id]

@router.post("/train")
async def start_training(config: TrainingConfig, background_tasks: BackgroundTasks):
    """启动模型训练"""
    try:
        # 检查模型是否存在
        if config.model_id not in models_db:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # 更新模型状态
        models_db[config.model_id]["status"] = "training"
        
        # 在后台任务中启动训练
        async def training_task():
            try:
                result = await mock_training_service.train_model(
                    model_id=config.model_id,
                    dataset=config.dataset,
                    batch_size=config.batch_size,
                    epochs=config.epochs,
                    learning_rate=config.learning_rate
                )
                # 更新模型状态
                models_db[config.model_id]["status"] = "trained"
                models_db[config.model_id]["accuracy"] = result["accuracy"]
                models_db[config.model_id]["best_model_path"] = result["best_model_path"]
            except Exception as e:
                models_db[config.model_id]["status"] = "error"
                models_db[config.model_id]["error"] = str(e)
        
        background_tasks.add_task(training_task)
        
        return {
            "message": "Training started",
            "model_id": config.model_id,
            "config": config.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/progress/{model_id}")
async def get_training_progress(model_id: str):
    """获取训练进度"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    progress = mock_training_service.get_training_progress(model_id)
    if progress["status"] == "not_found":
        return {"status": "not_started", "model_id": model_id}
    
    return progress

@router.get("/models/saved/{model_id}")
async def get_saved_models(model_id: str) -> List[Dict[str, Any]]:
    """获取指定模型的所有保存版本"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return mock_training_service.get_saved_models(model_id)

@router.get("/training/history")
async def get_all_training_history() -> List[Dict[str, Any]]:
    """获取所有训练历史"""
    return mock_training_service.get_training_history()

@router.get("/training/history/{model_id}")
async def get_model_training_history(model_id: str) -> List[Dict[str, Any]]:
    """获取模型的训练历史"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return mock_training_service.get_training_history(model_id=model_id)

@router.get("/training/history/{model_id}/{history_id}")
async def get_training_history_detail(model_id: str, history_id: str) -> Dict[str, Any]:
    """获取训练历史的详细信息"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    history = mock_training_service.get_training_history(history_id=history_id)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    
    return history

@router.post("/evaluate")
async def evaluate(request: EvaluationRequest) -> Dict[str, Any]:
    """评估模型性能"""
    try:
        result = await evaluate_model(
            model_path=request.model_path,
            dataset=request.dataset,
            batch_size=request.batch_size
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 