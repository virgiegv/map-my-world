from fastapi import Depends, HTTPException, Query, APIRouter, Response
from sqlalchemy.orm import Session
from . import crud, schemas

from src.db.database import get_db

router = APIRouter()


@router.post("/review/", tags=["reviews"], response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    result = crud.create_review(
        db, review=review
    )
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']


@router.get("/review/{review_id}", tags=["reviews"], response_model=schemas.Review)
def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    review = crud.get_review(db, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="review not found")
    return review


@router.get("/review/location/{location_id}", tags=["reviews"], response_model=list[schemas.Review])
def get_reviews_by_location_id(response: Response, location_id: int, db: Session = Depends(get_db)):
    result = crud.get_reviews_by_location(db, location_id)
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        response.status_code = result['status']
        return result['detail']


@router.get("/review/category/{category_id}", tags=["reviews"], response_model=list[schemas.Review])
def get_reviews_by_category_id(response: Response, category_id: int, db: Session = Depends(get_db)):
    result = crud.get_reviews_by_category(db, category_id)
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        response.status_code = result['status']
        return result['detail']


@router.get("/review", tags=["reviews"], response_model=list[schemas.Review])
def get_all_reviews(response: Response, db: Session = Depends(get_db)):
    result = crud.get_all_reviews(db)
    if (result is None) or (len(result) <= 0):
        response.status_code = 204
    else:
        response.status_code = 200
    return result


@router.delete("/review/{review_id}", tags=["reviews"])
def delete_review(review_id: int, db: Session = Depends(get_db)):
    affected_rows = crud.delete_review(db, review_id)
    if affected_rows <= 0:
        raise HTTPException(status_code=404, detail="review not found")
    return {"message": "Deleted"}


@router.put("/review/{review_id}", tags=["reviews"], response_model=schemas.Review)
def update_review_manual(review_id: int, review: schemas.ReviewUpdate,
                         db: Session = Depends(get_db)):
    result = crud.update_review_manually(db, review, review_id)
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']


@router.patch("/review/{review_id}", tags=["reviews"], response_model=schemas.Review)
def update_review_to_now(review_id: int, db: Session = Depends(get_db)):
    result = crud.update_review_to_now(db, review_id)
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']

