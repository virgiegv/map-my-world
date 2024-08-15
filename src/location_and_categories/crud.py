from sqlalchemy.orm import Session
from sqlalchemy import delete
from . import schemas
from ..db import models


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, category_name: str):
    return db.query(models.Category).filter(models.Category.name.ilike(f'%{category_name}%')).all()

def get_all_categories(db: Session):
    return db.query(models.Category).all()

def update_category(db: Session, category: schemas.CategoryUpdate, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        return 0
    else:
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
        return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        return 0
    locations = db_category.locations
    print(locations)
    for location in locations:
        location.category_id = None
    db.commit()
    db.refresh(db_category)

    db.delete(db_category)
    db.commit()
    return 1


def create_location(db: Session, location: schemas.LocationCreate, category_id: int = None):
    db_location = models.Location(**location.dict(), category_id=category_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_location_by_name(db: Session, location_name: str):
    return db.query(models.Location).filter(models.Location.name.ilike(f'%{location_name}%')).all()

def get_all_locations(db: Session):
    return db.query(models.Location).all()

def delete_location(db: Session, location_id: int):
    result = db.execute(delete(models.Location).where(models.Location.id == location_id))
    affected_rows = result.rowcount
    db.commit()
    return affected_rows

def update_location(db: Session, location: schemas.LocationUpdate,  location_id: int = None):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location is None:
        return 0
    else:
        db_location.name = location.name if (location.name is not None) else db_location.name
        db_location.longitude = location.longitude if (location.longitude is not None) else db_location.longitude
        db_location.latitude = location.latitude if (location.latitude is not None) else db_location.latitude
        db_location.category_id = location.category_id if (location.category_id is not None) else db_location.category_id

        db.commit()
        db.refresh(db_location)
        return db_location
