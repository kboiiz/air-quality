"""api routes"""
from config import Settings
from fastapi import FastAPI
from routers import air_data, stations
from shared_models import Base
from shared_models import stations_waqi, readings_waqi

settings = Settings()

app = FastAPI()


app.include_router(air_data.router)


app.include_router(stations.router)


@app.get("/")
def root():
    return {"message": "ah poop"}
