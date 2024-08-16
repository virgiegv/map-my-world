from pydantic import BaseModel
from datetime import datetime

class Recommendation(BaseModel):
    last_reviewed_date: datetime | None = None
    category: str
    location: str

class RecommendationWithIds(Recommendation):
    category_id: int
    location_id: int