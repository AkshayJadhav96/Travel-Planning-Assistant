import requests
from typing import List, Union
from pydantic import BaseModel, Field, ValidationError


API_KEY = "6ce5a5ead7204c8687860906252203"  # Replace with your API key
BASE_URL = "https://api.weatherapi.com/v1"


# Pydantic Models
class Condition(BaseModel):
    text: str


class Day(BaseModel):
    mintemp_c: float = Field(..., alias="mintemp_c")
    maxtemp_c: float = Field(..., alias="maxtemp_c")
    maxwind_kph: float = Field(..., alias="maxwind_kph")
    avghumidity: float = Field(..., alias="avghumidity")
    daily_chance_of_rain: int = Field(..., alias="daily_chance_of_rain")
    daily_chance_of_snow: int = Field(..., alias="daily_chance_of_snow")
    condition: Condition


class ForecastDay(BaseModel):
    date: str
    day: Day


class WeatherForecast(BaseModel):
    forecastday: List[ForecastDay]


def get_weather(city: str, days: int = 1) -> Union[List[dict], str]:
    """
    Fetches the weather forecast for a given city and future dates.
    Args:
        city (str): The name of the city.
        days (int): Number of future days for the forecast (1-14 days).
    Returns:
        Union[List[dict], str]: The weather forecast summary as a list of dictionaries or an error message.
    """

    # Use forecast endpoint for future weather
    endpoint = f"{BASE_URL}/forecast.json"
    params = {"key": API_KEY, "q": city, "days": days}

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        # Handle API errors
        if "error" in data:
            return f"Error: {data['error']['message']}"

        # Validate API response with Pydantic model
        try:
            forecast_data = WeatherForecast(forecastday=data["forecast"]["forecastday"])
        except ValidationError as e:
            return f"Error validating data: {e}"

        # Create a list of dictionaries with validated data
        forecast_summary = []
        for day in forecast_data.forecastday:
            forecast_summary.append({
                "date": day.date,
                "weather_desc": day.day.condition.text,
                "min_temp": f"{day.day.mintemp_c}°C",
                "max_temp": f"{day.day.maxtemp_c}°C",
                "wind_speed": f"{day.day.maxwind_kph} Kph",
                "humidity": f"{day.day.avghumidity}%",
                "rain_probability": f"{day.day.daily_chance_of_rain}%",
                "snow_probability": f"{day.day.daily_chance_of_snow}%"
            })

        return forecast_summary

    except Exception as e:
        return f"Error fetching weather data: {e}"


# Test: Get a 3-day forecast for Mumbai
print(get_weather("mumbai", days=3))
