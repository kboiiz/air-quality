"""airnow etl functions"""
from datetime import datetime as dt, timedelta
import os

import pandas as pd
import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-167.716404,3.233406,-63.653904,70.867976",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "0",
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
    }
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"


@dag(
    dag_id="airnow_etl",
    schedule=timedelta(minutes=10),
    start_date=dt(2022, 12, 2, 18, 39),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_etl():
    """
    First, creates temp table in postgres db. Then performs ETL of
    air quality data for all of USA for current observations."""
    create_temp_airnow_table = PostgresOperator(
        task_id="create_temp_airnow_temp_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_temp_airnow_data_table.sql",
    )

    @task
    def extract_current_data():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/aqi_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.get(
            AIRNOW_BY_STATION_API_URL, params=params, timeout=20
            )
        csv_data = response.text
        with open(data_path, 'w') as file:
            file.write(csv_data)

    def shape_airnow_data(df):
        """
        Uses .groupby() to split 'parameter' column into pm2.5 and pm10 groups.
        Then merge groups together under columns:

        site name | datetime | PM10 conc. | PM10 AQI |
        PM10 AQI cat. | PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
        """
        parameter_groups = df.groupby("parameter")
        pm10 = parameter_groups.get_group("PM10").drop(["parameter"], axis=1)
        pm10.rename(
            columns={
                "concentration": "pm_10_conc",
                "AQI": "pm_10_AQI",
                "AQI cat": "pm_10_cat"},
            inplace=True
        )
        pm2_5 = parameter_groups.get_group("PM2.5").drop(["parameter"], axis=1)
        pm2_5.rename(
            columns={
                "concentration": "pm_25_conc",
                "AQI": "pm_25_AQI",
                "AQI cat": "pm_25_AQI_cat"},
            inplace=True
        )
        merged_df = pd.merge(
            pm10,
            pm2_5,
            how="outer",
            on=["datetime", "station_name"],
            sort=False,
        )

        cols = merged_df.columns.tolist()
        cols = [cols[-4]] + cols[:4] + cols[-3:]
        merged_df = merged_df[cols]
        return merged_df

    @task
    def load_to_temp():
        """load new data to temp table"""
        column_names = [
            "latitude",
            "longitude",
            "datetime",
            "parameter",
            "concentration",
            "unit",
            "AQI",
            "AQI cat",
            "station_name",
            "agency name",
            "station id",
            "full station id", ]
        df = pd.read_csv(
            "/opt/airflow/dags/files/aqi_data.csv", names=column_names,
        )
        df.dropna(axis=0)
        df = df.drop(
            ["latitude", "longitude", "unit", "agency name", "station id",
             "full station id"],
            axis=1
        )
        merged_df = shape_airnow_data(df)
        merged_df = merged_df.replace({',': '-'}, regex=True)
        merged_df.to_csv('/opt/airflow/dags/files/aqi_data.csv', header=False, index=False)

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="COPY temp_airnow_data FROM stdin WITH DELIMITER AS ',' NULL AS ''",
            filename='/opt/airflow/dags/files/aqi_data.csv')

    @task
    def load_to_production():
        """upsert new data to the production table"""
        
        query = """
        INSERT INTO prod_airnow_data (
                station_name, reading_datetime, pm_10_conc, pm_10_AQI, 
                pm_10_AQI_CAT, pm_25_conc, pm_25_AQI, pm_25_AQI_CAT
                )
            SELECT * FROM temp_airnow_data
            ON CONFLICT DO NOTHING
        """
        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        conn = hook.get_conn()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return 0


    create_temp_airnow_table >> extract_current_data() >> load_to_temp() >> load_to_production()


dag = airnow_etl()