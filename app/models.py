from .database import Base
from sqlalchemy import Column, Integer, Float, String, Boolean, TIMESTAMP, text


class CellTower(Base):
    __tablename__ = 'cell_towers'
    cellid = Column(Integer, primary_key=True, nullable=False)
    mcc = Column(Integer,  nullable=False)
    radio = Column(String, nullable=False)
    net = Column(Integer,  nullable=False)
    range = Column(Integer,  nullable=False)
    samples = Column(Integer,  nullable=False)
    changable = Column(Boolean,  nullable=False)
    # created = Column(TIMESTAMP(timezone=True),
    #                     nullable=False, server_default=text("now()"))
    # updated = Column(TIMESTAMP(timezone=True),
    #                     nullable=False, server_default=text("now()"))
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    geo = Column(String, nullable=True)

class CellTowerCoverage(Base):
    __tablename__ = 'coverage'
    id = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    towers = Column(Integer,  nullable=False)