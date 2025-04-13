from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from services.evaluation import EvaluationService
from models.domain.model import Model
from models.schemas.evaluation import EvaluationRequest

router = APIRouter()
evaluation_service = EvaluationService()

@router.post("/evaluate/{model_id}")
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