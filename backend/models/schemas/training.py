from pydantic import BaseModel
from typing import Literal

class TrainingConfig(BaseModel):
    model_id: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int
    epochs: int
    learning_rate: float 