{{
    config(
        materialized="table",
        properties={
            "format": "'PARQUET'",
            "partitioning": "ARRAY['country', 'city']",

        },
        tags=["silver"]
    )
}}

with silver as (
    SELECT
        measurement_dt,
        CASE
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 0 AND 9 THEN date_trunc('hour', measurement_dt)
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 10 AND 19 THEN date_trunc('hour', measurement_dt) + interval '10' minute
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 20 AND 29 THEN date_trunc('hour', measurement_dt) + interval '20' minute
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 30 AND 39 THEN date_trunc('hour', measurement_dt) + interval '30' minute
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 40 AND 49 THEN date_trunc('hour', measurement_dt) + interval '40' minute
            WHEN EXTRACT(MINUTE FROM measurement_dt) BETWEEN 50 AND 59 THEN date_trunc('hour', measurement_dt) + interval '50' minute
        END AS measurement_dt_10m,
        country,
        city,
        temperature
    FROM {{ ref('silver') }}
)
select
    measurement_dt_10m,
    c.continent,
    c.country,
    city,
    round(avg(temperature), 2) as avg_10m_temperature
from silver
left join {{ ref('countries') }} as c
    on silver.country = c.country
group by measurement_dt_10m, c.continent, c.country, city
order by measurement_dt_10m, c.continent, c.country, city
