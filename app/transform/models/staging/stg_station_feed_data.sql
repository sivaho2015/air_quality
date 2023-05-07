WITH source AS (
    SELECT *
    FROM {{ source('air_quality', 'station_feed') }}
)
SELECT
    station_id::INTEGER,
    city_name,
    CASE
        WHEN latitude <> 'Unknown' THEN latitude::NUMERIC
    END AS latitude,
    CASE
        WHEN longitude <> 'Unknown' THEN longitude::NUMERIC
    END AS longitude,
    CASE
        WHEN local_measurement_time <> 'Unknown' THEN local_measurement_time::TIMESTAMP
    END AS local_measurement_time,
    CASE
        WHEN local_measurement_time <> 'Unknown' THEN local_measurement_time
    END AS local_measurement_timezone,
    CASE 
        WHEN local_measurement_timezone = '-07:00' THEN 'PST'
        WHEN local_measurement_timezone = '-06:00' THEN 'MST'
        WHEN local_measurement_timezone = '-05:00' THEN 'CST'
        WHEN local_measurement_timezone = '-04:00' THEN 'EST'
        WHEN local_measurement_timezone = '-03:00' THEN 'AST'
    END AS local_measurement_timezone_text,
    CASE
        WHEN carbon_monoxide <> 'Unknown' THEN carbon_monoxide::NUMERIC
    END AS carbon_monoxide,
    CASE
        WHEN humidity <> 'Unknown' THEN humidity::NUMERIC
    END AS humidity,
    CASE
        WHEN ozone <> 'Unknown' THEN ozone::NUMERIC
    END AS ozone,
    CASE
        WHEN pressure <> 'Unknown' THEN pressure::NUMERIC
    END AS pressure,
    CASE
        WHEN pm_10 <> 'Unknown' THEN pm_10::NUMERIC
    END AS pm_10,
    CASE
        WHEN pm_2_5 <> 'Unknown' THEN pm_2_5::NUMERIC
    END AS pm_2_5,
    CASE
        WHEN sulfur_dioxide <> 'Unknown' THEN sulfur_dioxide::NUMERIC
    END AS sulfur_dioxide,
    CASE
        WHEN temperature <> 'Unknown' THEN temperature::NUMERIC
    END AS temperature,
    CASE
        WHEN wind_speed <> 'Unknown' THEN wind_speed::NUMERIC
    END AS wind_speed
FROM source