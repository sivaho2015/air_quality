with source as (
    select *
    from {{ source('air_quality', 'station_feed') }}
)
select
    station_id::integer,
    city_name,
    case
        when latitude <> 'Unknown' then latitude::numeric
    end as latitude,
    case
        when longitude <> 'Unknown' then longitude::numeric
    end as longitude,
    case
        when local_measurement_time <> 'Unknown' then local_measurement_time::timestamp
    end as local_measurement_time,
    case
        when local_measurement_time <> 'Unknown' then local_measurement_time
    end as local_measurement_timezone,
    case 
        when local_measurement_timezone = '-07:00' then 'PST'
        when local_measurement_timezone = '-06:00' then 'MST'
        when local_measurement_timezone = '-05:00' then 'CST'
        when local_measurement_timezone = '-04:00' then 'EST'
        when local_measurement_timezone = '-03:00' then 'AST'
    end as local_measurement_timezone_text,
    case
        when carbon_monoxide <> 'Unknown' then carbon_monoxide::numeric
    end as carbon_monoxide,
    case
        when humidity <> 'Unknown' then humidity::numeric
    end as humidity,
    case
        when ozone <> 'Unknown' then ozone::numeric
    end as ozone,
    case
        when pressure <> 'Unknown' then pressure::numeric
    end as pressure,
    case
        when pm_10 <> 'Unknown' then pm_10::numeric
    end as pm_10,
    case
        when pm_2_5 <> 'Unknown' then pm_2_5::numeric
    end as pm_2_5,
    case
        when sulfur_dioxide <> 'Unknown' then sulfur_dioxide::numeric
    end as sulfur_dioxide,
    case
        when temperature <> 'Unknown' then temperature::numeric
    end as temperature,
    case
        when wind_speed <> 'Unknown' then wind_speed::numeric
    end as wind_speed
from source