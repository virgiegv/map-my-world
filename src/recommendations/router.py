from fastapi import Depends, HTTPException, Query, APIRouter, Response
from sqlalchemy.orm import Session
from . import recommendation

from src.db.database import get_db

router = APIRouter()


#@router.get("/recommend", tags="recommendations", )