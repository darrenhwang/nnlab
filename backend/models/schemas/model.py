from pydantic import BaseModel
from typing import List, Dict, Literal
from datetime import datetime

class Layer(BaseModel):
    id: str
    type: str
    units: int
    activation: str

class ModelBase(BaseModel):
    name: str
    layers: List[Layer]

class ModelCreate(ModelBase):
    id: str

class ModelResponse(ModelBase):
    id: str
    status: Literal['created', 'training', 'trained', 'error']
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True 