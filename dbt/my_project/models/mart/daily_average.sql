{{
    config(
        materialized='table'
    )
}}

SELECT 
    city,
    date(weather_time_local) AS date,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    ROUND(AVG(wind_speed)::numeric, 2) AS avg_wind_speed
FROM {{ ref('stg_weather_data') }}
GROUP BY city, date(weather_time_local)
ORDER BY city, date(weather_time_local)