from pydantic import BaseModel
from typing import Generic, TypeVar
from pydantic.generics import GenericModel

class CellTowerSchema(BaseModel):
    cellid: int
    mcc: int
    radio: str
    net: int
    range: int
    samples: int
    changable: bool
    lat: float
    lon: float
    # geo: str

    class Config:
        orm_mode = True

class CellTowerClosestSchema(BaseModel):
    cellid: int
    range: int
    lon: float
    lat: float
    radio: str
    operator: str
    operatorcode: int
    countryname: str
    countrycode: str

    class Config:
        orm_mode = True

class CellTowerCoverageSchema(BaseModel):
    id: int
    mcc: int
    radio_total: int
    radio_gsm: int
    radio_umts: int
    radio_lte: int
    countrycode: str
    geojson: str

    class Config:
        orm_mode = True


class CountrySchema(BaseModel):
    code: str
    name: str
    mcc: int
    hexagons: int
    center_lon: int
    center_lat: int
    box: str
    
    class Config:
        orm_mode = True