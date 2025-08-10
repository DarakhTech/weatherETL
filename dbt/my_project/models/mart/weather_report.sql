{{
    config(
        materialized='table',
        unique_key='id',
    )
}}

-- SELECT *
-- from {{ref('stg_weather_data')}}

-- with source as(
--     SELECT * 
--     FROM {{source('dev', 'raw_weather_data')}}
-- )


SELECT
    city,
    temperature,
    weather_description,
    wind_speed,
    weather_time_local
from {{ref('stg_weather_data')}}
