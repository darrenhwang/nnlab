from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

class TrainingHistory(BaseModel):
    id: str
    model_id: str
    dataset: str
    batch_size: int
    epochs: int
    learning_rate: float
    start_time: datetime
    end_time: datetime
    final_accuracy: float
    final_loss: float
    best_model_path: str
    metrics: List[Dict[str, Any]] 