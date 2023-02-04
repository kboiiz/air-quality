drop table if exists readings_airnow_temp;
create table readings_airnow_temp(
    station_name        varchar not null,
    request_datetime    timestamp not null,
    reading_datetime    timestamp not null,
    pm_10_conc          numeric(7,3),
    pm_10_aqi           numeric(7,3),
    pm_10_aqi_cat       numeric(2,1),
    pm_25_conc          numeric(7,3),
    pm_25_aqi           numeric(7,3),
    pm_25_aqi_cat       numeric(2,1)
);