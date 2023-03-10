"""crud functions"""
import math
from datetime import datetime

import pandas as pd
import pgeocode
from logger import LOGGER
from shared_models.pydantic_models import Location, PollutantEnum, TimeEnum
from shared_models.readings_airnow import ReadingsAirnow
from sqlalchemy import select, text
from sqlalchemy.orm import Session, load_only


def zipcode_to_latlong(zipcode: str) -> Location:
    """helper func returns tuple of lat long"""
    geo = pgeocode.Nominatim("us")
    loc = geo.query_postal_code(zipcode)
    if math.isnan(loc["latitude"]):
        return 1
    location = Location(lat=loc["latitude"], long=loc["longitude"])
    return location


def get_nearby_stations(zipcode: str, db: Session) -> list:
    """given zipcode, returns the 5 nearest stations"""
    loc = zipcode_to_latlong(zipcode)
    if loc == 1:
        return 1
    stmt = text(
        """
        SELECT station_id, station_name, agency_name, status, latitude, longitude, elevation, country
        FROM stations_airnow
        WHERE station_id IN (select station_id FROM readings_airnow)
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 5
        """
    )
    result = db.execute(stmt, {"x": loc.lat, "y": loc.long}).all()
    return result


def get_closest_station(zipcode: str, db: Session):
    """returns closest station to zipcode. note srid=4326 signifies data is of
    the latitude/longitude type."""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_id, station_name, agency_name, status, latitude, longitude, elevation, country
        FROM stations_airnow
        WHERE station_id IN (select station_id FROM readings_airnow)
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 1
        """
    )
    result = db.execute(stmt, {"x": loc.lat, "y": loc.long}).all()
    return result


def get_data(ids: list[str], db: Session, period: TimeEnum, pollutants: list[PollutantEnum]) -> list[dict]:
    """returns data for given station_ids, time period, and pollutants"""
    response = []
    columns = [pollutant.column() for pollutant in pollutants]
    with db.connection() as conn:
        for id in ids:
            stmt = (
                select(ReadingsAirnow)
                .options(load_only(*columns))
                .where(ReadingsAirnow.station_id == id and ReadingsAirnow.reading_datetime > period.start())
                .order_by(ReadingsAirnow.reading_datetime)
            )
            df = pd.read_sql_query(stmt, conn)
            df = (
                df.resample(period.letter(), on="reading_datetime")
                .mean(numeric_only=True)
                .round(decimals=0)
                .reset_index()
                .fillna(value=0)
            )
            j = df.to_dict(orient="records")
            response.append({"station_id": id, "readings": j})
    return response

