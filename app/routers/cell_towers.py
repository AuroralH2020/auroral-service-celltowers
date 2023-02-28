import chevron
from typing import List, Dict
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Response, status
from ..database import get_db
from sqlalchemy.sql import text
from ..scripts.query_templates import requestNearbyCells

router = APIRouter()

@router.get('/{mcc}', response_model=List[schemas.CellTowerSchema], status_code=status.HTTP_200_OK)
def get_towers(mcc: int, db: Session = Depends(get_db)):
    towers = db.query(models.CellTower).filter(models.CellTower.mcc == mcc).all()
    return towers

@router.get('/closest/', response_model=List[schemas.CellTowerClosestSchema], status_code=status.HTTP_200_OK)
def get_closest_towers(lat: float, lon: float, db: Session = Depends(get_db)):
    query = text(chevron.render(requestNearbyCells, {'lat': lat, 'lon': lon} ))
    towers = db.execute(query).all()
    return towers

@router.get('/closest/rdf-mapping', response_model=Dict, status_code=status.HTTP_200_OK)
def get_closest_towers_rdf_mapping(lat: float, lon: float, db: Session = Depends(get_db)):
    return Response(content={}, media_type="application/json")

@router.get('/coverage', response_model=List[schemas.CellTowerCoverageSchema], status_code=status.HTTP_200_OK)
def get_coverage(db: Session = Depends(get_db)):
    coverage = db.query(models.CellTowerCoverage).all()
    return coverage

