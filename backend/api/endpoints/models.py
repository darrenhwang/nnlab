from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.domain.model import Model
from models.schemas.model import ModelCreate, ModelResponse
from core.database import get_db

router = APIRouter()

@router.post("/", response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    db_model = Model(
        id=model.id,
        name=model.name,
        layers=model.layers,
        status="created"
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/", response_model=List[ModelResponse])
def get_models(db: Session = Depends(get_db)):
    return db.query(Model).all()

@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.delete("/{model_id}")
def delete_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(model)
    db.commit()
    return {"message": "Model deleted"} 