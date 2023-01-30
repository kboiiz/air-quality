from sqlalchemy import Column, DateTime, Numeric, String

from . import Base


class Readings_WAQI_Temp(Base):
    __tablename__ = 'readings_waqi_temp'

    station_name = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    request_datetime = Column(DateTime, nullable=False)
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    pm_10 = Column(Numeric(7, 3))
    pm_25 = Column(Numeric(7, 3))
    co = Column(Numeric(7, 3))
    h = Column(Numeric(7, 3))
    no2 = Column(Numeric(7, 3))
    o3 = Column(Numeric(7, 3))
    p = Column(Numeric(7, 3))
    so2 = Column(Numeric(7, 3))
    t = Column(Numeric(7, 3))
    w = Column(Numeric(7, 3))
    wg = Column(Numeric(7, 3))


class Readings_WAQI(Base):
    __tablename__ = 'readings_waqi'

    station_name = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    request_datetime = Column(DateTime, nullable=False)
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    pm_10 = Column(Numeric(7, 3))
    pm_25 = Column(Numeric(7, 3))
    co = Column(Numeric(7, 3))
    h = Column(Numeric(7, 3))
    no2 = Column(Numeric(7, 3))
    o3 = Column(Numeric(7, 3))
    p = Column(Numeric(7, 3))
    so2 = Column(Numeric(7, 3))
    t = Column(Numeric(7, 3))
    w = Column(Numeric(7, 3))
    wg = Column(Numeric(7, 3))
    