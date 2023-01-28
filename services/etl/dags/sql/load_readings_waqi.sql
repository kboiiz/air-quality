insert into air_quality.public.readings_waqi
(
    station_name,
    reading_datetime,
    request_datetime,
    latitude,
    longitude,
    pm_10,
    pm_25,
    co,
    h,
    no2,
    o3,
    p,
    so2,
    t,
    w,
    wg
)
select
    station_name,
    reading_datetime,
    request_datetime,
    latitude,
    longitude,
    pm_10,
    pm_25,
    co,
    h,
    no2,
    o3,
    p,
    so2,
    t,
    w,
    wg
from readings_waqi_temp
on conflict (station_name, reading_datetime) 
do update set
    station_name = excluded.station_name,
    reading_datetime = excluded.reading_datetime,
    request_datetime = excluded.request_datetime,
    latitude = excluded.latitude,
    longitude = excluded.longitude,
    pm_10 = excluded.pm_10,
    pm_25 = excluded.pm_25,
    co = excluded.co,
    h = excluded.h,
    no2 = excluded.no2,
    o3 = excluded.o3,
    p = excluded.p,
    so2 = excluded.so2,
    t = excluded.t,
    w = excluded.w,
    wg = excluded.wg