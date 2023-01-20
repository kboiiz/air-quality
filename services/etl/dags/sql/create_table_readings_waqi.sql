create table if not exists air_quality.public.readings_waqi(
            station_name varchar not null,
            reading_datetime timestamp not null,
            request_datetime timestamp not null,
            latitude    numeric(10,6),
            longitude   numeric(10,6),
            pm_10       numeric(7,3),
            pm_25       numeric(7,3),
            co          numeric(7,3),
            h           numeric(7,3),
            no2         numeric(7,3),
            o3          numeric(7,3),
            p           numeric(7,3),
            so2         numeric(7,3),
            t           numeric(7,3),
            w           numeric(7,3),
            wg          numeric(7,3),
            primary key (station_name, reading_datetime)
);