import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from typing import Dict, Any


def get_weather(latitude: float, longitude: float, target_date: str, start_hour: int, timezone: str = None) -> Dict[str, Any]:
    """
    Fetch historical weather data for a specific location, date, and hour.

    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        target_date (str): Date in YYYY-MM-DD format
        start_hour (int): Hour of the day (0-23)
        timezone (str, optional): Timezone name. Defaults to None (UTC).

    Returns:
        Dict[str, Any]: Weather data including temperature, precipitation, wind, etc.
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # API request parameters
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": target_date,
        "end_date": target_date,
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation",
            "cloud_cover",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "is_day"
        ],
        "timezone": timezone.upper() if timezone else "UTC"
    }

    # Make API request
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }

    # Add weather variables
    hourly_data.update({
        "temperature_c": hourly.Variables(0).ValuesAsNumpy(),
        "apparent_temperature_c": hourly.Variables(1).ValuesAsNumpy(),
        "precipitation": hourly.Variables(2).ValuesAsNumpy(),
        "cloud_cover": hourly.Variables(3).ValuesAsNumpy(),
        "wind_speed": hourly.Variables(4).ValuesAsNumpy(),
        "wind_direction": hourly.Variables(5).ValuesAsNumpy(),
        "wind_gusts": hourly.Variables(6).ValuesAsNumpy(),
        "is_day": hourly.Variables(7).ValuesAsNumpy()
    })

    # Convert to DataFrame and filter for specific hour
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe = hourly_dataframe[hourly_dataframe['date'].dt.hour == start_hour]

    # Format time
    hourly_dataframe['time'] = hourly_dataframe['date'].dt.strftime('%H:%M')

    # Convert wind direction to compass direction
    directions = [
        "North", "North-Northeast", "Northeast", "East-Northeast",
        "East", "East-Southeast", "Southeast", "South-Southeast",
        "South", "South-Southwest", "Southwest", "West-Southwest",
        "West", "West-Northwest", "Northwest", "North-Northwest"
    ]

    # Get the first (and only) row
    row = hourly_dataframe.iloc[0]

    # Create formatted return dictionary
    weather_data = {
        "time": row['time'],
        "period": "Day" if row['is_day'] == 1 else "Night",
        "temperature": {
            "celsius": int(row['temperature_c']),
            "feels_like": int(row['apparent_temperature_c'])
        },
        "precipitation_mm": int(row['precipitation']),
        "cloud_cover_percent": int(row['cloud_cover']),
        "wind": {
            "speed": {
                "kmh": int(row['wind_speed']),
                "mph": int(row['wind_speed'] * 0.621371)
            },
            "direction": directions[int((row['wind_direction'] % 360) / 22.5)],
            "gusts": {
                "kmh": int(row['wind_gusts']),
                "mph": int(row['wind_gusts'] * 0.621371)
            }
        }
    }

    return weather_data
