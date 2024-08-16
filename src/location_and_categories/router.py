from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from src.location_and_categories import crud, schemas

from src.db.database import get_db

router = APIRouter()


@router.post("/category/{name}", tags=["categories"], response_model=schemas.Category)
def create_category(name: str, db: Session = Depends(get_db)):
    result = crud.create_category(db, category=schemas.CategoryCreate(name=name))
    print(result)
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']


@router.get("/category/", tags=["categories"], response_model=list[schemas.Category])
def get_category_by_name(name: str = Query(None), db: Session = Depends(get_db)):
    if name is None:
        return crud.get_all_categories(db)
    return crud.get_category_by_name(db, name)


@router.get("/category/{category_id}", tags=["categories"], response_model=schemas.Category)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/category/{category_id}", tags=["categories"], response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    update_result = crud.update_category(db, category, category_id)
    if update_result['error']:
        raise HTTPException(status_code=update_result['status'], detail=update_result['detail'])
    return update_result['detail']


@router.delete("/category/{category_id}", tags=["categories"],)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    affected_rows = crud.delete_category(db, category_id)
    if affected_rows <= 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Deleted"}


@router.post("/category/{category_id}/location", tags=["categories", "locations"], response_model=schemas.Location)
def create_location_for_category(category_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    result = crud.create_location(
        db, location=location, category_id=category_id
    )
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']


@router.post("/location/", tags=["locations"], response_model=schemas.Location)
def create_location_without_category(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    result = crud.create_location(
        db, location=location
    )
    if result['error']:
        raise HTTPException(status_code=result['status'], detail=result['detail'])
    else:
        return result['detail']


@router.get("/location/{location_id}", tags=["locations"], response_model=schemas.Location)
def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.get("/location/", tags=["locations"], response_model=list[schemas.Location])
def get_location_by_name(name: str = Query(None), db: Session = Depends(get_db)):
    if name is None:
        return crud.get_all_locations(db)
    return crud.get_location_by_name(db, name)


@router.delete("/location/{location_id}", tags=["locations"])
def delete_location(location_id: int, db: Session = Depends(get_db)):
    affected_rows = crud.delete_location(db, location_id)
    if affected_rows <= 0:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Deleted"}


@router.put("/location/{location_id}", tags=["locations"], response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationUpdate, db: Session = Depends(get_db)):
    update_result = crud.update_location(db, location, location_id)

    if update_result['error']:
        raise HTTPException(status_code=update_result['status'], detail=update_result['detail'])
    else:
        return update_result['detail']
