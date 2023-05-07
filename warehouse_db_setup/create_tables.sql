-- Set up a table that stores air quality data from API
DROP SCHEMA IF EXISTS air_quality;
CREATE SCHEMA air_quality;
DROP TABLE IF EXISTS air_quality.station_feed;
CREATE TABLE air_quality.station_feed (
    station_id VARCHAR(300),
    city_name VARCHAR(300),
    latitude VARCHAR(100),
    longitude VARCHAR(100),
    local_measurement_time VARCHAR(300),
    local_measurement_timezone VARCHAR(100),
    carbon_monoxide VARCHAR(100),
    humidity VARCHAR(100),
    ozone VARCHAR(100),
    pressure VARCHAR(100),
    pm_10 VARCHAR(100),
    pm_2_5 VARCHAR(100),
    sulfur_dioxide VARCHAR(100),
    temperature VARCHAR(100),
    wind_speed VARCHAR(100)
);