{{
    config(
        materialized="incremental",
        properties={
            "format": "'PARQUET'",
            "partitioning": "ARRAY['country', 'city', 'hour(measurement_dt)']"
        },
        tags=["bronze"]
    )
}}

with raw as (
    select
        timestamp,
        from_iso8601_timestamp(json_query(value, 'strict $.timestamp'  OMIT QUOTES)) as measurement_dt,
        json_query(value, 'strict $.country'  OMIT QUOTES) as country,
        json_query(value, 'strict $.city'  OMIT QUOTES) as city,
        cast(json_query(value, 'strict $.temperature'  OMIT QUOTES) as double) as temperature
    from {{ source('raw_data','weather_raw') }}
)
select
    timestamp,
    measurement_dt,
    country,
    city,
    temperature
from raw
{% if is_incremental() %}
where timestamp >= (select coalesce(max(timestamp),cast('1900-01-01' as timestamp(6))) from {{ this }})
{% endif %}
