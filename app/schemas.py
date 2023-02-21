import datetime
from pydantic import BaseModel


class CellTowerSchema(BaseModel):
    cellid: int
    mcc: int
    radio: str
    net: int
    range: int
    samples: int
    changable: bool
    # created = datetime
    # updated = datetime
    lat: float
    lon: float
    geo: str

    class Config:
        orm_mode = True

class CellTowerCoverageSchema(BaseModel):
    id: int
    lat: float
    lon: float
    towers: int

    class Config:
        orm_mode = True