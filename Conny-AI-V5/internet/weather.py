import requests


class WeatherEngine:
    """
    CONNY AI Weather Engine V1

    Gets current weather information
    from the Open-Meteo public API.
    """

    def __init__(self, timeout=10):

        self.timeout = timeout

        self.last_location = ""
        self.last_result = None

    # ==================================================
    # MAIN WEATHER FUNCTION
    # ==================================================

    def get_weather(self, location):

        location = str(location).strip()

        if not location:
            return None

        self.last_location = location

        try:

            # ------------------------------------------
            # Geocoding
            # ------------------------------------------

            geo_url = (
                "https://geocoding-api.open-meteo.com/v1/search"
            )

            geo_params = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            response = requests.get(
                geo_url,
                params=geo_params,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            results = data.get(
                "results",
                []
            )

            if not results:

                print(
                    "DEBUG WeatherEngine: "
                    "LOCATION NOT FOUND"
                )

                return None

            place = results[0]

            latitude = place.get(
                "latitude"
            )

            longitude = place.get(
                "longitude"
            )

            name = place.get(
                "name",
                location
            )

            country = place.get(
                "country",
                ""
            )

            # ------------------------------------------
            # Weather
            # ------------------------------------------

            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
            )

            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            }

            response = requests.get(
                weather_url,
                params=weather_params,
                timeout=self.timeout
            )

            response.raise_for_status()

            weather = response.json()

            current = weather.get(
                "current"
            )

            if not current:

                print(
                    "DEBUG WeatherEngine: "
                    "NO WEATHER DATA"
                )

                return None

            result = {
                "location": name,
                "country": country,
                "temperature": current.get(
                    "temperature_2m"
                ),
                "feels_like": current.get(
                    "apparent_temperature"
                ),
                "humidity": current.get(
                    "relative_humidity_2m"
                ),
                "wind_speed": current.get(
                    "wind_speed_10m"
                ),
                "weather_code": current.get(
                    "weather_code"
                )
            }

            self.last_result = result

            print(
                "DEBUG WeatherEngine: SUCCESS"
            )

            return result

        except Exception as error:

            print(
                "DEBUG WeatherEngine Error:",
                error
            )

            return None

    # ==================================================
    # WEATHER DESCRIPTION
    # ==================================================

    def describe_weather(self, code):

        descriptions = {

            0: "Clear sky",

            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",

            45: "Fog",
            48: "Depositing rime fog",

            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",

            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",

            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",

            66: "Light freezing rain",
            67: "Heavy freezing rain",

            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",

            77: "Snow grains",

            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",

            85: "Slight snow showers",
            86: "Heavy snow showers",

            95: "Thunderstorm",

            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }

        return descriptions.get(
            code,
            "Unknown conditions"
        )

    # ==================================================
    # FORMAT RESPONSE
    # ==================================================

    def format_weather(self, result):

        if not result:
            return None

        location = result.get(
            "location",
            "Unknown"
        )

        country = result.get(
            "country",
            ""
        )

        temperature = result.get(
            "temperature"
        )

        feels_like = result.get(
            "feels_like"
        )

        humidity = result.get(
            "humidity"
        )

        wind = result.get(
            "wind_speed"
        )

        code = result.get(
            "weather_code"
        )

        description = self.describe_weather(
            code
        )

        place = location

        if country:

            place += (
                f", {country}"
            )

        return (
            f"Current weather in {place}:\n\n"
            f"Condition: {description}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind} km/h"
        )
