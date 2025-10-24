"""
Weather Data Integration Module
Handles API calls to OpenWeatherMap and data parsing
"""
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import Config


class WeatherService:
    """Service for fetching and processing weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize weather service with API key"""
        self.api_key = api_key or Config.OPENWEATHER_API_KEY
        if not self.api_key:
            print("WARNING: OpenWeatherMap API key is not set. Please set OPENWEATHER_API_KEY in .env file")
            print("Get your free API key at: https://openweathermap.org/api")
        else:
            print(f"Weather service initialized with API key: {self.api_key[:8]}...")
        
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """
        Get current weather data for a location
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing current weather data
        """
        url = f"{Config.OPENWEATHER_BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if 'cod' in data and data['cod'] != 200:
                raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
            
            return self._parse_current_weather(data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid API key. Please check your OPENWEATHER_API_KEY in .env file")
            elif e.response.status_code == 404:
                raise Exception("Location not found")
            else:
                raise Exception(f"HTTP Error {e.response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch current weather: {str(e)}")
    
    def get_forecast(self, lat: float, lon: float, days: int = 5) -> List[Dict]:
        """
        Get weather forecast for a location
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days to forecast (default 5)
            
        Returns:
            List of daily forecast dictionaries
        """
        url = Config.OPENWEATHER_FORECAST_URL
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if 'cod' in data and str(data['cod']) != '200':
                raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
            
            return self._parse_forecast(data, days)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid API key. Please check your OPENWEATHER_API_KEY in .env file")
            elif e.response.status_code == 404:
                raise Exception("Location not found")
            else:
                raise Exception(f"HTTP Error {e.response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch forecast: {str(e)}")
    
    def get_weather_by_city(self, city: str) -> Dict:
        """
        Get current weather by city name
        
        Args:
            city: City name
            
        Returns:
            Dictionary containing weather data
        """
        url = f"{Config.OPENWEATHER_BASE_URL}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_current_weather(data)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather for {city}: {str(e)}")
    
    def _parse_current_weather(self, data: Dict) -> Dict:
        """Parse OpenWeatherMap current weather response"""
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'] * 3.6,  # Convert m/s to km/h
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'description': data['weather'][0]['description'],
            'main': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'rain_1h': data.get('rain', {}).get('1h', 0),
            'rain_3h': data.get('rain', {}).get('3h', 0),
            'snow_1h': data.get('snow', {}).get('1h', 0),
            'timestamp': datetime.fromtimestamp(data['dt']),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'city': data['name'],
            'country': data['sys']['country'],
            'coordinates': {
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            }
        }
    
    def _parse_forecast(self, data: Dict, days: int) -> List[Dict]:
        """Parse OpenWeatherMap forecast response"""
        forecasts = []
        daily_data = {}
        
        # Group by date
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date = dt.date()
            
            if date not in daily_data:
                daily_data[date] = []
            
            daily_data[date].append({
                'datetime': dt,
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'] * 3.6,
                'description': item['weather'][0]['description'],
                'main': item['weather'][0]['main'],
                'icon': item['weather'][0]['icon'],
                'clouds': item['clouds']['all'],
                'rain': item.get('rain', {}).get('3h', 0),
                'snow': item.get('snow', {}).get('3h', 0),
            })
        
        # Aggregate daily data
        for date, items in sorted(daily_data.items())[:days]:
            temps = [i['temperature'] for i in items]
            forecasts.append({
                'date': date,
                'temp_min': min(temps),
                'temp_max': max(temps),
                'temp_avg': sum(temps) / len(temps),
                'humidity_avg': sum(i['humidity'] for i in items) / len(items),
                'wind_speed_max': max(i['wind_speed'] for i in items),
                'total_rain': sum(i['rain'] for i in items),
                'total_snow': sum(i['snow'] for i in items),
                'description': items[len(items)//2]['description'],  # Mid-day description
                'icon': items[len(items)//2]['icon'],
                'details': items
            })
        
        return forecasts
    
    def get_uv_index(self, lat: float, lon: float) -> Optional[float]:
        """
        Get UV index for a location (requires One Call API)
        Note: One Call API 3.0 requires subscription
        """
        # For free tier, we'll return None
        # Implement if you have One Call API access
        return None
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get air quality data for a location
        """
        url = f"{Config.OPENWEATHER_BASE_URL}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['list']:
                aqi_data = data['list'][0]
                return {
                    'aqi': aqi_data['main']['aqi'],  # 1-5 scale
                    'components': aqi_data['components'],
                    'timestamp': datetime.fromtimestamp(aqi_data['dt'])
                }
        except Exception:
            return None
