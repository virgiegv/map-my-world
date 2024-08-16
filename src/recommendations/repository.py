from sqlalchemy.orm import Session
from src.db import models
from sqlalchemy import distinct, not_, and_, func, asc
from datetime import datetime, timedelta, UTC


def get_categories_never_reviewed(db: Session):
    # first we get the list of categories that have been reviewed
    reviewed_categories = db.query(distinct(models.LocationCategoryReview.category_id)).all()
    reviewed_category_ids = [row[0] for row in reviewed_categories]

    # now we get the categories that havent been reviewed
    never_reviewed_categories = db.query(models.Category).filter(models.Category.id.notin_(reviewed_category_ids)).all()
    return never_reviewed_categories


def get_locations_without_categories(db: Session, categories_to_exclude):
    # from the list of categories to exclude we get the ids into another list
    categories_to_exclude_ids = [category.id for category in categories_to_exclude]

    # locations that have been reviewed
    reviewed_locations = db.query(distinct(models.LocationCategoryReview.location_id)).all()
    reviewed_locations_ids = [row[0] for row in reviewed_locations]

    # locations that haven't been reviewed and are not in the categories to exclude
    never_reviewed_locations = db.query(models.Location).filter(
        and_(
            models.Location.id.notin_(reviewed_locations_ids),
            models.Location.category_id.notin_(categories_to_exclude_ids)
        )
    ).all()
    return never_reviewed_locations


def get_top_N_reviews_not_updated_in_a_month(db: Session, n: int):
    thirty_days_ago = datetime.now(UTC) - timedelta(days=30)

    reviews = db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.last_reviewed_date <= thirty_days_ago).order_by(
        asc(models.LocationCategoryReview.last_reviewed_date)).limit(n).all()

    return reviews

