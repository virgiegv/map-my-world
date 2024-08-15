from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from . import crud, schemas

from src.db.database import get_db

router = APIRouter()

@router.post("/review/", tags=["reviews"], response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(
        db, review=review
    )