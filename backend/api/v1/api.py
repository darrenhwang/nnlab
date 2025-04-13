from fastapi import APIRouter
from api.endpoints import models, training, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(models.router, prefix="/models", tags=["模型"])
api_router.include_router(training.router, prefix="/training", tags=["训练"]) 