from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    latitude: float
    longitude: float
    name: str | None = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    name: str | None = None
    category_id: Optional[int] = None

class Location(LocationBase):
    id: int
    category_id: Optional[int] = None



class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    locations: list[Location] = []

    class Config:
        from_attributes = True

