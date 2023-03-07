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
    towers = db.query(models.CellTower).filter(
        models.CellTower.mcc == mcc).all()
    return towers


@router.get('/closest/', response_model=List[schemas.CellTowerClosestSchema], status_code=status.HTTP_200_OK)
def get_closest_towers(lat: float, lon: float, db: Session = Depends(get_db)):
    query = text(chevron.render(requestNearbyCells, {'lat': lat, 'lon': lon}))
    towers = db.execute(query).all()
    return towers


@router.get('/closest/rdf-mapping', response_model=List, status_code=status.HTTP_200_OK)
def get_closest_towers_rdf_mapping(lat: float, lon: float, db: Session = Depends(get_db)):
    query = text(chevron.render(requestNearbyCells, {'lat': lat, 'lon': lon}))
    towers: schemas.CellTowerClosestSchema = db.execute(query).all()
    content = [{
        "@context": [
            "https://auroralh2020.github.io/auroral-ontology-contexts/cellTowers/context.json",
            {
                "distance": {
                    "@id": "https://auroral.iot.linkeddata.es/def/adapters#Distance",
                    "@type": "http://www.w3.org/2001/XMLSchema#integer"
                }
            },
        ],
        "cellId": "{0}".format(tower[0]),
        "hasRange": {
            "range": "{0}".format(tower[2])
        },
        "location": {
            "lat": tower[4],
            "long": tower[5]
        },
        "distance": tower[1]
    } for tower in towers]
    return content


@router.get('/coverage/{mcc}', response_model=List[schemas.CellTowerCoverageSchema], status_code=status.HTTP_200_OK)
def get_coverage(mcc: int, db: Session = Depends(get_db)):
    coverage = db.query(models.CellTowerCoverage).filter(
        models.CellTowerCoverage.mcc == mcc).all()
    return coverage
