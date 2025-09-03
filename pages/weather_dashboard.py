import streamlit as st
import requests

st.title("🌦️ Real-Time Weather (No API Key)")

city = st.text_input("Enter a city name:", "London")

# Simple mapping from Open-Meteo weather codes to text + emoji
WEATHER_CODES = {
    0:  ("Clear sky", "🌞"),
    1:  ("Mainly clear", "🌤️"),
    2:  ("Partly cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌧️"),
    57: ("Dense freezing drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌧️"),
    67: ("Heavy freezing rain", "🌧️"),
    71: ("Slight snow fall", "🌨️"),
    73: ("Moderate snow fall", "🌨️"),
    75: ("Heavy snow fall", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌦️"),
    82: ("Violent rain showers", "🌧️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with slight hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
}

def geocode_city(name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 1, "language": "en", "format": "json"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    top = results[0]
    return {
        "name": top.get("name"),
        "lat": top.get("latitude"),
        "lon": top.get("longitude"),
        "country": top.get("country"),
        "admin1": top.get("admin1"),
    }
    
def get_current_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,  # returns temperature, windspeed, winddirection, weathercode, time
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh",
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("current_weather")

if st.button("Get Weather"):
    try:
        place = geocode_city(city.strip())
        if not place:
            st.error("City not found. Try a more specific name (e.g., 'Paris, Texas').")
        else:
            wx = get_current_weather(place["lat"], place["lon"])
            if not wx:
                st.error("Could not retrieve current weather for that location.")
            else:
                code = int(wx.get("weathercode", -1))
                desc, emoji = WEATHER_CODES.get(code, ("Unknown", "❓"))
                temp = wx.get("temperature")
                wind = wx.get("windspeed")
                time = wx.get("time")

                loc_line = place["name"]
                if place.get("admin1"):
                    loc_line += f", {place['admin1']}"
                if place.get("country"):
                    loc_line += f", {place['country']}"

                st.subheader(f"Weather in {loc_line}")
                st.write(f"Observed at: {time}")
                st.write(f"Temperature: {temp} °C")
                st.write(f"Wind: {wind} km/h")
                st.write(f"Condition: {desc} {emoji}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        
