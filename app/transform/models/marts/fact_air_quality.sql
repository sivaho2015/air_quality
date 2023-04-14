{{
    config(
        materialized='incremental'
    )
}}
with station_feed as (
    select *
    from {{ ref('stg_station_feed_data') }}
)
select
    station_id,
    local_measurement_time,
    local_measurement_timezone_text,
    carbon_monoxide,
    humidity,
    ozone,
    pressure,
    pm_10,
    pm_2_5,
    sulfur_dioxide,
    temperature,
    wind_speed
from station_feed

{% if is_incremental() %}

where date(local_measurement_time) > (select max(date(local_measurement_time)) from {{ this }})

{% endif %}