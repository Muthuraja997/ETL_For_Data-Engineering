import requests
import pandas as pd
from datetime import datetime
import snowflake.connector
import os


SNOWFLAKE_USER = '############'
SNOWFLAKE_PASSWORD = '############'
SNOWFLAKE_ACCOUNT = '#############'
SNOWFLAKE_DATABASE = 'WEATHER_DB'
SNOWFLAKE_SCHEMA = 'PUBLIC'
SNOWFLAKE_WAREHOUSE = 'COMPUTE_WH'
SNOWFLAKE_TABLE = 'WEATHER_DATA'

city_name = "Coimbatore"
API_KEY = "######################"
full_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={API_KEY}"

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32

def fetch_data():
    response = requests.get(full_url)
    return response.json()

def transform_data(data):
    return {
        "City": data["name"],
        "Description": data["weather"][0]['description'],
        "Temperature_F": kelvin_to_fahrenheit(data["main"]["temp"]),
        "Feels_Like_F": kelvin_to_fahrenheit(data["main"]["feels_like"]),
        "Minimum_Temp_F": kelvin_to_fahrenheit(data["main"]["temp_min"]),
        "Maximum_Temp_F": kelvin_to_fahrenheit(data["main"]["temp_max"]),
        "Pressure": data["main"]["pressure"],
        "Humidity": data["main"]["humidity"],
        "Wind_Speed": data["wind"]["speed"],
        "Time_of_Record": datetime.utcfromtimestamp(data['dt'] + data['timezone']),
        "Sunrise_Local_Time": datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']),
        "Sunset_Local_Time": datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
    }

def load_to_snowflake(record):
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cs = conn.cursor()

    cs.execute(f"""
        CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
            City STRING,
            Description STRING,
            Temperature_F FLOAT,
            Feels_Like_F FLOAT,
            Minimum_Temp_F FLOAT,
            Maximum_Temp_F FLOAT,
            Pressure INTEGER,
            Humidity INTEGER,
            Wind_Speed FLOAT,
            Time_of_Record TIMESTAMP,
            Sunrise_Local_Time TIMESTAMP,
            Sunset_Local_Time TIMESTAMP
        )
    """)

    insert_query = f"""
        INSERT INTO {SNOWFLAKE_TABLE} VALUES (
            %(City)s, %(Description)s, %(Temperature_F)s, %(Feels_Like_F)s,
            %(Minimum_Temp_F)s, %(Maximum_Temp_F)s, %(Pressure)s,
            %(Humidity)s, %(Wind_Speed)s, %(Time_of_Record)s,
            %(Sunrise_Local_Time)s, %(Sunset_Local_Time)s
        )
    """
    cs.execute(insert_query, record)
    cs.close()
    conn.close()

def run_weather_etl():
    data = fetch_data()
    transformed = transform_data(data)
    load_to_snowflake(transformed)
