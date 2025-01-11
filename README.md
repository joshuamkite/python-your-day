# Python Your Day

This project combines several independent scripts into a modular Python application, serving as a demonstration in structuring multi-file Python projects. It fetches historical weather data from [open-meteo](https://open-meteo.com/), calculates the day of the week for any date (since 1754), and retrieves historical events that occurred on that date from [Wikimedia](https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day). The functionality is equivalent to the [React/Next.js version running on my website](https://www.joshuakite.co.uk/historical-day/index.html) with [code on GitHub](https://github.com/joshuamkite/react-your-day).

- [Historical Weather and Events Application](#historical-weather-and-events-application)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Technical Notes](#technical-notes)
    - [Module Organization](#module-organization)
    - [Key Components](#key-components)
  - [Dependencies](#dependencies)
  - [Features Demonstrated](#features-demonstrated)
  - [Application Data Flow](#application-data-flow)

## Project Structure

```
historical_date_app/
├── __init__.py
├── main.py
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── weather_service.py
│   ├── date_calculator.py
│   └── wiki_events.py
└── utils/
    ├── __init__.py
    ├── cities.py
    └── date_validator.py
```

## Features

- Historical weather data retrieval using Open-Meteo API
- Day of week calculation for dates after 1754 (Gregorian calendar) using Zeller's congruence
- Wikipedia events lookup for a given date
- Interactive city selection from major world cities
- Command-line interface with dropdown menus

## Installation

1. Clone the repository
2. Create and activate a virtual environment (recommended)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

Follow the interactive prompts to:
1. Enter a date (YYYY-MM-DD)
2. Select a city from the dropdown menu
3. Choose an hour of the day

The application will display:
- The day of the week for that date
- Historical weather conditions for the selected location and time
- Notable events that occurred on that date for various years in history

## Technical Notes

### Module Organization
This project demonstrates several Python project structuring concepts:
- Package organization with `__init__.py` files
- Separation of concerns between modules
- Use of utility modules for shared functionality
- Type hints and dataclasses for improved code clarity

### Key Components
- `weather_service.py`: Handles API interactions with Open-Meteo
- `date_calculator.py`: Implements day of week calculation algorithm
- `wiki_events.py`: Manages Wikipedia API interactions
- `cities.py`: Provides city data structure using dataclasses
- `date_validator.py`: Handles date validation and parsing

## Dependencies

- openmeteo-requests: Weather API client
- requests-cache: API response caching
- pandas: Data manipulation
- questionary: Interactive CLI interface
- requests: HTTP client for Wikipedia API

## Features Demonstrated

This project demonstrates:
1. Converting single-file scripts into a modular application
2. Proper Python package structure
3. Using dataclasses for structured data
4. Interactive CLI development
5. API integration and error handling
6. Code organization and reusability

## Application Data Flow

```mermaid
flowchart TD
    subgraph User_Input
        UI[User Interface]
        UI --> |Date| DV[Date Validator]
        UI --> |City| CD[Cities Data]
        UI --> |Hour| TI[Time Input]
    end

    subgraph Core_Processing
        DV --> DCW[Date Component Worker]
        CD --> |City Coordinates| DCW
        TI --> DCW
        
        DCW --> |Validated Date| DC[Date Calculator]
        DCW --> |Date + Coordinates + Hour| WS[Weather Service]
        DCW --> |Month/Day| WE[Wiki Events]
    end

    subgraph External_Services
        WS <--> |Historical Weather Query| OM[Open-Meteo API]
        WE <--> |Historical Events Query| WA[Wikipedia API]
    end

    subgraph Results
        DC --> |Day of Week| Main[Result Aggregator]
        WS --> |Weather Data| Main
        WE --> |Events Data| Main
        Main --> Display[Formatted Output]
    end

    classDef input fill:#e1f5fe,stroke:#01579b
    classDef core fill:#f3e5f5,stroke:#4a148c
    classDef external fill:#fff3e0,stroke:#e65100
    classDef results fill:#fce4ec,stroke:#880e4f

    class UI,CD,TI,DV input
    class DCW,DC,WS,WE core
    class OM,WA external
    class Main,Display results
 ```
