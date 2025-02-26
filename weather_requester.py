from datetime import datetime

import requests
from dotenv import load_dotenv
import os
import sqlalchemy as db

load_dotenv()

API_KEY = os.environ['WEATHER_API_KEY']
url = "https://archive-api.open-meteo.com/v1/archive"
WMO_CODES = {
	"0": "Солнечно",
	"1": "В основном солнечно",
	"2": "Переменная облачность",
	"3": "Облачно",
	"45": "Туманно",
	"48": "Изморозь",
	"51": "Небольшая морось",
	"53": "Морось",
	"55": "Сильная морось",
	"56": "Небольшая ледяная морось",
	"57": "Ледяная морось",
	"61": "Небольшой дождь",
	"63": "Дождь",
	"65": "Сильный дождь",
	"66": "Небольшой ледяной дождь",
	"67": "Ледяной дождь",
	"71": "Небольшой снег",
	"73": "Снег",
	"75": "Сильный снег",
	"77": "Снежная крупа",
	"80": "Небольшие ливни",
	"81": "Ливни",
	"82": "Сильные ливни",
	"85": "Небольшие снегопады",
	"86": "Снегопады",
	"95": "Гроза",
	"96": "Слабая гроза с градом",
	"99": "Гроза с градом"
}

latitude = '55.7522'
longitude = '37.6156'

daily='weather_code,temperature_2m_mean'
timezone='Europe/Moscow'

def weather_table_inject(date):
	response = requests.request("GET", url, params={
		'latitude':latitude,
		'longitude':longitude,
		'daily':daily,
		'timezone':timezone,
		'start_date': date,
		'end_date': date})
	print(response.json())
	res = (date,
		   float(response.json()["daily"]["temperature_2m_mean"][0]),
		   str(WMO_CODES[str(response.json()["daily"]["weather_code"][0])]))
	insert_weather_data(res)

def insert_weather_data(data):
	engine = db.create_engine(
		"postgresql://neondb_owner:npg_FBvTi18ySpoY@ep-yellow-salad-a9lbdmij-pooler.gwc.azure.neon.tech/neondb?sslmode=require")

	with engine.connect() as connection:
		query = db.text(f"""
	            INSERT INTO weather (date, temperature, info) 
	            VALUES (:val1, :val2, :val3)
	        """)
		connection.execute(query, {"val1": data[0], "val2": data[1], "val3": data[2]})
		connection.commit()
