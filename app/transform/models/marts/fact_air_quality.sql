{{
    config(
        materialized='incremental'
    )
}}
WITH station_feed AS (
    SELECT *
    FROM {{ ref('stg_station_feed_data') }}
)
SELECT
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
FROM station_feed

{% if is_incremental() %}

WHERE DATE(local_measurement_time) > (SELECT max(DATE(local_measurement_time)) FROM {{ this }})

{% endif %}