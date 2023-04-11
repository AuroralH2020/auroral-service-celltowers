import chevron
from typing import List, Dict
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Response, status
from ..database import get_db
from sqlalchemy.sql import text
from ..scripts.query_templates import requestNearbyCells

router = APIRouter()


@router.get('/country/{mcc}', response_model=List[schemas.CellTowerSchema], status_code=status.HTTP_200_OK)
def get_towers(mcc: int, db: Session = Depends(get_db)):
    towers = db.query(models.CellTower).filter(
        models.CellTower.mcc == mcc).all()
    return towers


@router.get('/closest', response_model=List[schemas.CellTowerClosestSchema], status_code=status.HTTP_200_OK)
def get_closest_towers(lat: float, lon: float, db: Session = Depends(get_db)):
    query = text(chevron.render(requestNearbyCells, {'lat': lat, 'lon': lon}))
    towers = db.execute(query).all()
    return towers


@router.get('/closest/rdf-mapping', response_model=List, status_code=status.HTTP_200_OK)
def get_closest_towers_rdf_mapping(lat: float, lon: float, db: Session = Depends(get_db)):
    query = text(chevron.render(requestNearbyCells, {'lat': lat, 'lon': lon}))
    towers = db.execute(query).all()
    print(towers)
    content = [{
        "@context": [
            "https://auroralh2020.github.io/auroral-ontology-contexts/cellTowers/context.json",
            {
                "dcterms": "http://purl.org/dc/terms/"
            }
        ],
        "dcterms:rights": "https://opencellid.org/",
        "dcterms:license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "cellId": f"{tower[0]}",
        "hasRange": {
            "range": f"{tower[2]}"
        },
        "hasOperator": {
            "operatorId": f"{tower[8]}",
            "operatorName": f"{tower[7]}",
        },
        "country": {
            "code": f"{tower[9]}",
            "name": f"{tower[10]}",
        },
        "location": {
            "lat": tower[5],
            "long": tower[6]
        },
        "providesNetwork":{
            "@type": f"{tower[3]}"
        }
    } for tower in towers]
    return content


@router.get('/coverage/{mcc}', response_model=List[schemas.CellTowerCoverageSchema], status_code=status.HTTP_200_OK)
def get_coverage(mcc: int, db: Session = Depends(get_db)):
    coverage = db.query(models.CellTowerCoverage).filter(
        models.CellTowerCoverage.mcc == mcc).all()
    return coverage
