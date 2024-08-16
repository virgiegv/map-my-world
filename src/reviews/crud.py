from sqlalchemy.orm import Session
from sqlalchemy import delete, desc
from . import schemas
from ..db import models
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import pytz

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.LocationCategoryReview(**review.dict())

    try:
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
    except IntegrityError as e:
        if 'unique constraint' in str(e.orig).lower():
            return {
                "error": True,
                "detail": "duplicated review entry",
                "status": 400
            }
        else:
            return {
                "error": True,
                "detail": "unexpected error occurred",
                "status": 500
            }

    return {"error": False, "detail": db_review}


def get_review(db: Session, review_id: int):
    return db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == review_id).first()


def get_reviews_by_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        return {
            "error": True,
            "detail": "category not found",
            "status": 404
        }

    query = db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.category_id == category_id).order_by(
        desc(models.LocationCategoryReview.last_reviewed_date)).all()

    return {
        "error": False,
        "status": 204 if len(query) <= 0 else 200,
        "detail": query
    }


def get_reviews_by_location(db: Session, location_id: int):
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        return {
            "error": True,
            "detail": "location not found",
            "status": 404
        }

    query = db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.location_id == location_id).order_by(
        desc(models.LocationCategoryReview.last_reviewed_date)).all()

    return {
        "error": False,
        "status": 204 if len(query) <= 0 else 200,
        "detail": query
    }


def get_all_reviews(db: Session):
    return db.query(models.LocationCategoryReview).order_by(
        desc(models.LocationCategoryReview.last_reviewed_date)).all()


#
def delete_review(db: Session, review_id: int):
    result = db.execute(delete(models.LocationCategoryReview).where(models.LocationCategoryReview.id == review_id))
    affected_rows = result.rowcount
    db.commit()
    return affected_rows


def update_review_manually(db: Session, review: schemas.ReviewUpdate, review_id: int):
    db_review = db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == review_id).first()
    if db_review is None:
        return {
            "error": True,
            "detail": "review not found",
            "status": 404
        }
    else:
        try:
            db_review.category_id = review.category_id if (review.category_id is not None) else db_review.category_id
            db_review.location_id = review.location_id if (review.location_id is not None) else db_review.location_id
            db_review.last_reviewed_date = review.last_reviewed_date if (
                        review.last_reviewed_date is not None) else db_review.last_reviewed_date

            db.commit()
            db.refresh(db_review)

        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower():
                return {
                    "error": True,
                    "detail": "update would violate review unique constraint",
                    "status": 400
                }
            else:
                return {
                    "error": True,
                    "detail": "unexpected error occurred",
                    "status": 500
                }

        return {"error": False, "detail": db_review}


def update_review_to_now(db: Session, review_id: int):
    db_review = db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == review_id).first()
    if db_review is None:
        return {
            "error": True,
            "detail": "review not found",
            "status": 404
        }
    else:
        db_review.last_reviewed_date = datetime.now(tz=pytz.utc)
        db.commit()
        db.refresh(db_review)

        return {"error": False, "detail": db_review}


