from pydantic import BaseModel
from typing import Literal

class EvaluationRequest(BaseModel):
    model_path: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int = 64 