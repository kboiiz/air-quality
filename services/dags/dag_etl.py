"""daang look at that dag, it ETL"""

from datetime import datetime as dt, timedelta
import json

import requests
from sqlalchemy import (
    create_engine, text, MetaData, Table, Column, DateTime, Integer, String, ForeignKey,
    select, insert)
from sqlalchemy.orm import Session, relationship, registry, sessionmaker
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

params = {
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
    "zipCode": 11206,
    "format": "application/json"}
CURRENT_ZIP_BY_URL = "https://www.airnowapi.org/aq/observation/zipCode/current/"

mapper_registry = registry()
Base = mapper_registry.generate_base()

class RawAirDataPoint(Base):
    __tablename__ = "raw_air_data_point"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    aqi = Column(String, nullable=False)

    def __repr__(self):
        return f"RawAirDataPoin(id={self.id!r}, timestamp={self.timestamp!r}, aqi={self.aqi!r}"

@dag(
    dag_id="etl",
    schedule=timedelta(minutes=1),
    start_date=dt(2022, 12, 4, 20, 24),
    catchup=False,
    dagrun_timeout=timedelta(minutes=20),
)
def etl():
    hook = PostgresHook(postgres_conn_id="etl_pg_conn")
    engine = hook.get_sqlalchemy_engine()
    Session = sessionmaker(engine)

    @task
    def create_airnow_temp_table():
        mapper_registry.metadata.create_all(engine)

    @task
    def extract_current_data():
        time = dt.now()
        response = requests.get(CURRENT_ZIP_BY_URL, params=params, timeout=10)
        json_data = json.loads(response.text)
        ozone_aqi = json_data[0]["AQI"]
        new_data_point = RawAirDataPoint()
        new_data_point.timestamp = time
        new_data_point.aqi = ozone_aqi
        with Session() as session:
            session.add(new_data_point)
            session.commit()

    setup = create_airnow_temp_table()
    ingest = extract_current_data()

etl()