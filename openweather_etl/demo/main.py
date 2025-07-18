import json 
from datetime import datetime
import pandas as pd
import requests 

city_name="Coimbatore"
base_url="https://api.openweathermap.org/data/2.5/weather?q="

with open("credentials.txt","r") as file:
    api_key=file.read()
full_url=base_url+city_name+"&APPID="+api_key
r=requests.get(full_url)
# print(r)
data=r.json()
city = data["name"]
weather_description = data["weather"][0]['description']
temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
pressure = data["main"]["pressure"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
