from fastapi import APIRouter
import requests
from csv import writer

router = APIRouter(
	prefix='/weather',
	tags=['weather']
)


@router.get("/get_weather_data")
def fetch_weather_data():
	url = "https://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q=city&days=1"
	response = requests.get(url)
	
	if response.status_code == 200:
		data = response.json()
		with open('time', "w") as csvfile:
			csvwriter = writer(csvfile)
			csvwriter.writerows(str(data))

		return {"message": "Weather data fetched and saved successfully!"}
	else:
		return {"error": "Failed to fetch weather data"}