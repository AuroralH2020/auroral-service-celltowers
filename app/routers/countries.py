from typing import List
from sqlalchemy.sql import text
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from ..database import get_db
from ..scripts.query_templates import groupCountries

router = APIRouter()

@router.get('/', response_model=List[schemas.CountrySchema], status_code=status.HTTP_200_OK)
def get_all_countries(db: Session = Depends(get_db)):
    query = text(groupCountries)
    countries = db.execute(query).all()
    return countries

