{{
    config(
        materialized='incremental',
        unique_key='station_id',
        incremental_strategy='delete+insert'
    )
}}
WITH station_feed AS (
    SELECT *
    FROM {{ ref('stg_station_feed_data') }}
)
SELECT DISTINCT
    station_id,
    local_measurement_timezone_text,
    city_name,
    latitude,
    longitude
FROM station_feed