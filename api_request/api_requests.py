import requests
import os
# Getting API key from .env file
api_key = os.getenv("API_KEY")
api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query=New York'

def fetch_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response received successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise
    
# fetch_data()

def mock_fetch_data():
    return {"request":{"type":"City","query":"New York, United States of America","language":"en","unit":"m"},"location":{"name":"New York","country":"United States of America","region":"New York","lat":"40.714","lon":"-74.006","timezone_id":"America\/New_York","localtime":"2025-07-23 19:32","localtime_epoch":1753299120,"utc_offset":"-4.0"},"current":{"observation_time":"11:32 PM","temperature":24,"weather_code":113,"weather_icons":["https:\/\/cdn.worldweatheronline.com\/images\/wsymbols01_png_64\/wsymbol_0001_sunny.png"],"weather_descriptions":["Sunny"],"astro":{"sunrise":"05:45 AM","sunset":"08:20 PM","moonrise":"03:57 AM","moonset":"08:01 PM","moon_phase":"Waning Crescent","moon_illumination":4},"air_quality":{"co":"338.55","no2":"31.635","o3":"82","so2":"7.215","pm2_5":"17.76","pm10":"20.535","us-epa-index":"2","gb-defra-index":"2"},"wind_speed":24,"wind_degree":168,"wind_dir":"SSE","pressure":1024,"precip":0,"humidity":52,"cloudcover":0,"feelslike":26,"uv_index":0,"visibility":16,"is_day":"yes"}}