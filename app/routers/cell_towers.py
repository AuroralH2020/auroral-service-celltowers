from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from ..database import get_db

router = APIRouter()

@router.get('/', response_model=List[schemas.CellTowerSchema], status_code=status.HTTP_200_OK)
def get_all_towers(db: Session = Depends(get_db)):
    towers = db.query(models.CellTower).all()
    return towers

@router.get('/coverage', response_model=List[schemas.CellTowerCoverageSchema], status_code=status.HTTP_200_OK)
def get_all_towers(db: Session = Depends(get_db)):
    coverage = db.query(models.CellTowerCoverage).all()
    return coverage

