from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    last_reviewed_date: datetime | None = None
    category_id: int
    location_id: int
    class Config:
        from_attributes = True

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    last_reviewed_date: datetime | None = None
    category_id: int | None = None
    location_id: int | None = None

class Review(ReviewBase):
    id: int
