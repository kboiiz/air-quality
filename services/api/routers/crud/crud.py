"""crud functions"""
import pgeocode
from sqlalchemy import text
from sqlalchemy.orm import Session
from geoalchemy2 import Geometry


def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return loc["latitude"], loc["longitude"]


def get_nearby_stations(zipcode: str, db: Session):
    """given zipcode, returns the 5 nearest stations"""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_name, latitude, longitude, location_coord
        FROM stations_airnow
        ORDER BY location_coord <-> 'SRID=4326;POINT(:x :y)'::geometry
        LIMIT 5
        """
    )
    result = db.execute(stmt, {'x': loc[0], 'y': loc[1]}).all()
    return result


def get_closest_station(zipcode: str, db: Session):
    """given zipcode, returns the closest station. note srid=4326 signifies
    that the data is of the latitude/longitude type."""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_name, latitude, longitude, location_coord
        FROM stations_airnow
        ORDER BY location_coord <-> 'SRID=4326;POINT(:x :y)'::geometry
        LIMIT 1
        """
    )
    result = db.execute(stmt, {'x': loc[0], 'y': loc[1]}).all()
    return result


def get_data(station: str, db: Session):
    stmt = text(
        """
        SELECT
            station_name,
            reading_datetime,
            pm_10_conc,
            pm_10_AQI,
            pm_10_AQI_CAT,
            pm_25_conc,
            pm_25_AQI,
            pm_25_AQI_CAT
        FROM airnow_readings
        WHERE station_name = :x
        ORDER BY reading_datetime"""
    )
    data = db.execute(stmt, {"x": station}).all()
    return data
