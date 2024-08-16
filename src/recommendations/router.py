from fastapi import Depends, HTTPException, Query, APIRouter, Response
from sqlalchemy.orm import Session
from . import recommendation
from . import schemas
from src.db.database import get_db

router = APIRouter()


@router.get("/recommend", tags=["recommendations"], response_model=list[schemas.Recommendation])
def recommend(db: Session = Depends(get_db)):
    return recommendation.get_recommendations(db)