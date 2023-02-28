from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from ..database import get_db

router = APIRouter()

@router.get('/', response_model=List[schemas.CountrySchema], status_code=status.HTTP_200_OK)
def get_all_countries(db: Session = Depends(get_db)):
    countries = db.query(models.Country).order_by(models.Country.name).all()
    return countries

