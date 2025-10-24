"""
Configuration module for Weather App
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    IPINFO_API_KEY = os.getenv('IPINFO_API_KEY', '')
    
    # API Endpoints
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    OPENWEATHER_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    # App Settings
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Weather thresholds for agriculture
    AGRICULTURE_THRESHOLDS = {
        'wind_speed_spray': 20,  # km/h - max wind for pesticide spraying
        'rain_threshold': 10,     # mm - significant rainfall
        'frost_temp': 2,          # °C - frost warning
        'heat_stress': 35,        # °C - heat stress for crops
        'high_humidity': 80,      # % - disease risk
    }
    
    # Travel recommendations thresholds
    TRAVEL_THRESHOLDS = {
        'cold_weather': 10,       # °C
        'hot_weather': 30,        # °C
        'rain_warning': 5,        # mm
        'wind_warning': 40,       # km/h
    }
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr']
    DEFAULT_LANGUAGE = 'en'
