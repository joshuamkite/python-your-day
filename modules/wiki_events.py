import requests


def get_historical_events(month: int, day: int) -> list:
    """Fetch historical events from Wikipedia API."""
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/{month}/{day}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data.get('events', [])
    else:
        raise Exception("Failed to fetch Wikipedia events")
