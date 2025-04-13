from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.domain.model import Model
from models.schemas.training import TrainingConfig
from core.database import get_db
from services.training import train_model
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, model_id: str):
        await websocket.accept()
        self.active_connections[model_id] = websocket

    def disconnect(self, model_id: str):
        if model_id in self.active_connections:
            del self.active_connections[model_id]

    async def send_update(self, model_id: str, data: dict):
        if model_id in self.active_connections:
            await self.active_connections[model_id].send_json(data)

manager = ConnectionManager()

@router.post("/start")
async def start_training(config: TrainingConfig, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == config.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model.status = "training"
    db.commit()
    
    # 启动训练任务
    asyncio.create_task(train_model(config, model, db, manager))
    
    return {"message": "Training started"}

@router.websocket("/ws/training/{model_id}")
async def websocket_endpoint(websocket: WebSocket, model_id: str):
    await manager.connect(websocket, model_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(model_id) 