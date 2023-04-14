{{
    config(
        materialized='incremental',
        unique_key='station_id',
        incremental_strategy='delete+insert'
    )
}}
with station_feed as (
    select *
    from {{ ref('stg_station_feed_data') }}
)
select distinct
    station_id,
    local_measurement_timezone_text,
    city_name,
    latitude,
    longitude
from station_feed