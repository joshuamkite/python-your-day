# main.py
import questionary
from datetime import datetime
from modules.weather_service import get_weather
from modules.date_calculator import get_day_of_week
from modules.wiki_events import get_historical_events
from utils.date_validator import validate_date
from utils.cities import get_major_cities, City


def get_user_inputs():
    """Get user inputs using interactive prompts."""
    # Get date
    date_str = questionary.text(
        "Enter a date",
        default=datetime.now().strftime("%Y-%m-%d"),
        validate=lambda text: validate_date_input(text)
    ).ask()

    # Get city selection
    cities = get_major_cities()
    city_choices = [city.name for city in cities]
    selected_city_name = questionary.select(
        "Select a city",
        choices=city_choices,
    ).ask()
    selected_city = next(city for city in cities if city.name == selected_city_name)

    # Get hour selection
    hour = questionary.select(
        "Select hour",
        choices=[f"{str(h).zfill(2)}:00" for h in range(24)],
        default="12:00"
    ).ask()
    hour = int(hour.split(":")[0])

    return date_str, selected_city, hour


def validate_date_input(text):
    """Validate date input."""
    try:
        validate_date(text)
        return True
    except ValueError as e:
        return str(e)


def main():
    try:
        # Get user inputs using interactive CLI
        date_str, selected_city, hour = get_user_inputs()

        print(f"\nFetching historical information for {selected_city.name} on {date_str}...")

        # Get and validate date object
        date = validate_date(date_str)

        # Print day of week
        day = get_day_of_week(date_str)
        print(f"\nThat date was a {day}")

        # Get and print weather
        try:
            weather = get_weather(selected_city.lat, selected_city.lon, date_str, hour)
            print("\nHistorical Weather Conditions:")
            print(f"Time: {hour:02d}:00")
            print(f"Period: {weather['period']}")
            print(f"Temperature: {weather['temperature']['celsius']}°C (feels like {weather['temperature']['feels_like']}°C)")
            print(f"Precipitation: {weather['precipitation_mm']} mm")
            print(f"Cloud Cover: {weather['cloud_cover_percent']}%")
            print(f"Wind Speed: {weather['wind']['speed']['kmh']} km/h ({weather['wind']['speed']['mph']} mph)")
            print(f"Wind Direction: {weather['wind']['direction']}")
            print(f"Wind Gusts: {weather['wind']['gusts']['kmh']} km/h ({weather['wind']['gusts']['mph']} mph)")
        except Exception as e:
            print(f"Could not fetch weather data: {e}")

        # Get and print historical events
        try:
            events = get_historical_events(date.month, date.day)
            if events:
                print("\nHistorical Events On This Day:")
                for event in events:
                    print(f"{event['year']}: {event['text']}")
        except Exception as e:
            print(f"Could not fetch historical events: {e}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return


if __name__ == "__main__":
    main()
