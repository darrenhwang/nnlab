from pydantic import BaseModel
from typing import Literal, Optional

class EvaluationRequest(BaseModel):
    """评估请求模型"""
    model_path: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int = 64

class TrainingConfig(BaseModel):
    """训练配置模型"""
    model_id: str
    dataset: Literal['mnist', 'cifar10', 'fashion_mnist']
    batch_size: int
    epochs: int
    learning_rate: float

class Model:
    """模拟模型类"""
    @staticmethod
    def get(model_id):
        """获取模型静态方法"""
        return {
            "id": model_id,
            "name": f"Model {model_id}",
            "type": "CNN",
            "created_at": "2025-04-13"
        } 