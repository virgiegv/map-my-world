from sqlalchemy.orm import Session
from sqlalchemy import delete
from . import schemas
from ..db import models
from datetime import datetime


def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.LocationCategoryReview(**review.dict())

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int):
    return db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == review_id).first()


def get_review_by_category(db: Session, category_id: int):
    return db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.category_id == category_id).all()


def get_review_by_location(db: Session, location_id: int):
    return db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.location_id == location_id).all()


def get_all_reviews(db: Session):
    return db.query(models.LocationCategoryReview).all()
#
def delete_review(db: Session, review_id: int):
    result = db.execute(delete(models.LocationCategoryReview).where(models.LocationCategoryReview.id == review_id))
    affected_rows = result.rowcount
    db.commit()
    return affected_rows
#
# def update_location(db: Session, location: schemas.LocationUpdate,  location_id: int = None):
#     db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
#     if db_location is None:
#         return 0
#     else:
#         db_location.name = location.name if (location.name is not None) else db_location.name
#         db_location.longitude = location.longitude if (location.longitude is not None) else db_location.longitude
#         db_location.latitude = location.latitude if (location.latitude is not None) else db_location.latitude
#         db_location.category_id = location.category_id if (location.category_id is not None) else db_location.category_id
#
#         db.commit()
#         db.refresh(db_location)
#         return db_location
