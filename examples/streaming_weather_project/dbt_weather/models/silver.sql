{{
    config(
        materialized="table",
        properties={
            "format": "'PARQUET'",
            "partitioning": "ARRAY['country', 'city', 'hour(measurement_dt)']"
        },
        tags=["silver"]
    )
}}

with bronze as (
    select
        timestamp,
        measurement_dt,
        country,
        city,
        temperature,
        ROW_NUMBER() OVER (PARTITION by measurement_dt, country, city ORDER BY timestamp DESC) as rn
    FROM {{ ref('bronze') }}
)
select
    measurement_dt,
    country,
    city,
    temperature
from bronze
where rn = 1
order by measurement_dt, country, city, timestamp desc
