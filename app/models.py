from .database import Base
from sqlalchemy import Column, Integer, Float, String, Boolean
from geoalchemy2 import Geometry


class CellTower(Base):
    __tablename__ = 'cell_towers'
    cellid = Column(Integer, primary_key=True, nullable=False)
    mcc = Column(Integer,  nullable=False)
    radio = Column(String, nullable=False)
    net = Column(Integer,  nullable=False)
    range = Column(Integer,  nullable=False)
    samples = Column(Integer,  nullable=False)
    changable = Column(Boolean,  nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    geo = Column(Geometry('POLYGON'))

class CellTowerCoverage(Base):
    __tablename__ = 'coverage'
    id = Column(Integer, primary_key=True, nullable=False)
    radio_total = Column(Integer,  nullable=False)
    radio_gsm = Column(Integer,  nullable=False)
    radio_umts = Column(Integer,  nullable=False)
    radio_lte = Column(Integer,  nullable=False)
    countrycode = Column(String, nullable=False)
    geom = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)


class Country(Base):
    __tablename__ = 'countries'
    code = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    mcc = Column(Integer,  nullable=False)
    geo = Column(String, nullable=False)