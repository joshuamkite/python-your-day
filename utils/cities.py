# utils/cities.py

from dataclasses import dataclass
from typing import List


@dataclass
class City:
    name: str
    lat: float
    lon: float


def get_major_cities() -> List[City]:
    """Returns a list of major cities with their coordinates."""
    return [
        # Europe
        City("London, UK", 51.5074, -0.1278),
        City("Paris, France", 48.8566, 2.3522),
        City("Berlin, Germany", 52.5200, 13.4050),
        City("Madrid, Spain", 40.4168, -3.7038),
        City("Rome, Italy", 41.9028, 12.4964),
        City("Amsterdam, Netherlands", 52.3676, 4.9041),
        City("Moscow, Russia", 55.7558, 37.6173),
        City("Istanbul, Turkey", 41.0082, 28.9784),

        # North America
        City("New York, USA", 40.7128, -74.0060),
        City("Los Angeles, USA", 34.0522, -118.2437),
        City("Chicago, USA", 41.8781, -87.6298),
        City("Toronto, Canada", 43.6532, -79.3832),
        City("Vancouver, Canada", 49.2827, -123.1207),
        City("Mexico City, Mexico", 19.4326, -99.1332),

        # Asia
        City("Tokyo, Japan", 35.6762, 139.6503),
        City("Beijing, China", 39.9042, 116.4074),
        City("Shanghai, China", 31.2304, 121.4737),
        City("Hong Kong", 22.3193, 114.1694),
        City("Singapore", 1.3521, 103.8198),
        City("Seoul, South Korea", 37.5665, 126.9780),
        City("Mumbai, India", 19.0760, 72.8777),
        City("Dubai, UAE", 25.2048, 55.2708),

        # Oceania
        City("Sydney, Australia", -33.8688, 151.2093),
        City("Melbourne, Australia", -37.8136, 144.9631),
        City("Auckland, New Zealand", -36.8509, 174.7645),

        # South America
        City("São Paulo, Brazil", -23.5505, -46.6333),
        City("Rio de Janeiro, Brazil", -22.9068, -43.1729),
        City("Buenos Aires, Argentina", -34.6037, -58.3816),
        City("Lima, Peru", -12.0464, -77.0428),

        # Africa
        City("Cairo, Egypt", 30.0444, 31.2357),
        City("Cape Town, South Africa", -33.9249, 18.4241),
        City("Lagos, Nigeria", 6.5244, 3.3792),
        City("Nairobi, Kenya", -1.2921, 36.8219)
    ]


def get_city_by_name(name: str) -> City:
    """Returns a city object by its name."""
    cities = get_major_cities()
    for city in cities:
        if city.name == name:
            return city
    raise ValueError(f"City '{name}' not found")
