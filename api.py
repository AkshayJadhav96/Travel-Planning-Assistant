from fastapi import FastAPI, HTTPException
from tools.Currency import convert_currency
from tools.flights import search_flights
from tools.hotels import search_hotels
from tools.Weather import get_weather
from tools.pydantic_models import FlightSearchRequest, FlightSearchResponse, HotelSearchRequest, HotelSearchResponse

app = FastAPI(
    title="Travel Planning API",
    description="API for currency conversion, flight search, hotel search, and weather forecasts",
    version="1.0.0"
)

# Currency Conversion Endpoint
@app.get("/currency/convert")
def convert_currency_endpoint(amount: float, from_currency: str, to_currency: str):
    """
    Convert an amount from one currency to another.
    
    Args:
        amount (float): The amount to convert.
        from_currency (str): Source currency code (e.g., 'USD').
        to_currency (str): Target currency code (e.g., 'EUR').
    
    Returns:
        dict: Converted amount or error message.
    """
    result = convert_currency(amount, from_currency, to_currency)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Flight Search Endpoint
@app.post("/flights/search", response_model=FlightSearchResponse)
def search_flights_endpoint(request: FlightSearchRequest):
    """
    Search for flights based on the provided criteria.
    
    Args:
        request (FlightSearchRequest): Flight search parameters.
    
    Returns:
        FlightSearchResponse: List of flight options or error/message.
    """
    result = search_flights(request)
    if result.error:
        raise HTTPException(status_code=400, detail=result.error)
    return result

# Hotel Search Endpoint
@app.post("/hotels/search", response_model=HotelSearchResponse)
def search_hotels_endpoint(request: HotelSearchRequest):
    """
    Search for hotels based on the provided criteria.
    
    Args:
        request (HotelSearchRequest): Hotel search parameters.
    
    Returns:
        HotelSearchResponse: List of hotel options or error/message.
    """
    result = search_hotels(request)
    if result.error:
        raise HTTPException(status_code=400, detail=result.error)
    return result

# Weather Forecast Endpoint
@app.get("/weather/forecast")
def get_weather_endpoint(city: str, days: int = 1):
    """
    Get the weather forecast for a given city and number of days.
    
    Args:
        city (str): The name of the city.
        days (int): Number of future days for the forecast (default is 1, max 14).
    
    Returns:
        list: Weather forecast summary or error message.
    """
    result = get_weather(city, days)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)