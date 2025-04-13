from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import asyncio
import os
from ..models.schemas.training import TrainingConfig
from ..services.training import TrainingService
from ..services.model import ModelService
from ..models.domain.model import Model
from ..services.training_history import TrainingHistoryService

router = APIRouter()
training_service = TrainingService()
model_service = ModelService()
history_service = TrainingHistoryService()

# 存储训练进度
training_progress: Dict[str, Dict[str, Any]] = {}

async def progress_callback(model_id: str, progress: Dict[str, Any]):
    """更新训练进度"""
    training_progress[model_id] = progress

@router.post("/train")
async def start_training(config: TrainingConfig, background_tasks: BackgroundTasks):
    try:
        # 获取模型
        model = model_service.get_model(config.model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # 启动训练任务
        background_tasks.add_task(
            training_service.train_model,
            config,
            model,
            lambda p: progress_callback(config.model_id, p)
        )
        
        return {"message": "Training started", "model_id": config.model_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/progress/{model_id}")
async def get_training_progress(model_id: str):
    """获取训练进度"""
    if model_id not in training_progress:
        raise HTTPException(status_code=404, detail="No training progress found")
    return training_progress[model_id]

@router.get("/models/saved/{model_id}")
async def get_saved_models(model_id: str) -> List[Dict[str, Any]]:
    """获取指定模型的所有保存版本"""
    try:
        models_dir = "saved_models"
        if not os.path.exists(models_dir):
            return []
            
        # 获取所有匹配的模型文件
        model_files = []
        for filename in os.listdir(models_dir):
            if filename.startswith(model_id):
                # 解析文件名获取信息
                parts = filename.split('_')
                if len(parts) >= 4:
                    timestamp = parts[1]
                    epoch = parts[2].replace('epoch', '')
                    accuracy = parts[3].replace('acc', '').replace('.pth', '')
                    
                    model_files.append({
                        'filename': filename,
                        'timestamp': timestamp,
                        'epoch': int(epoch),
                        'accuracy': float(accuracy),
                        'path': os.path.join(models_dir, filename)
                    })
        
        # 按时间戳排序
        model_files.sort(key=lambda x: x['timestamp'], reverse=True)
        return model_files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/history/{model_id}")
async def get_training_history(model_id: str) -> List[Dict[str, Any]]:
    """获取模型的训练历史"""
    try:
        histories = history_service.get_model_history(model_id)
        return [history.dict() for history in histories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/history/{model_id}/{history_id}")
async def get_training_history_detail(model_id: str, history_id: str) -> Dict[str, Any]:
    """获取训练历史的详细信息"""
    try:
        history = history_service.get_history(history_id)
        if history.model_id != model_id:
            raise HTTPException(status_code=404, detail="History not found")
        return history.dict()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="History not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 