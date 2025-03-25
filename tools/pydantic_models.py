from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class FlightSearchRequest(BaseModel):
    source: str = Field(..., min_length=3, max_length=3, description="IATA code of the departure airport")
    destination: str = Field(..., min_length=3, max_length=3, description="IATA code of the destination airport")
    date: str = Field(..., pattern="\\d{4}-\\d{2}-\\d{2}", description="Travel date in 'YYYY-MM-DD' format")
    adults: int = Field(1, gt=0, description="Number of adult passengers")
    currency: str = Field("USD", min_length=3, max_length=3, description="Currency code for price display")

class FlightOption(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: str

class FlightSearchResponse(BaseModel):
    flights: List[FlightOption] = []
    message: Optional[str] = None
    error: Optional[str] = None

class HotelSearchRequest(BaseModel):
    city_code: str = Field(..., min_length=3, max_length=3, description="IATA city code")
    radius: int = Field(10, ge=1, description="Search radius around city center (default: 10 km)")
    radius_unit: Literal["KM", "MI"] = Field("KM", description="Unit of radius (KM or MI)")
    amenities: Optional[str] = Field(None, description="Comma-separated list of amenities")
    ratings: Optional[str] = Field(None, description="Comma-separated list of minimum ratings")

class HotelOption(BaseModel):
    name: str
    hotel_id: Optional[str]
    address: Optional[str]
    rating: Optional[str]
    amenities: List[str]

class HotelSearchResponse(BaseModel):
    hotels: Optional[List[HotelOption]] = None
    message: Optional[str] = None
    error: Optional[str] = None
