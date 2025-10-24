"""
Location Detection Module
Handles location detection via IP and GPS coordinates
"""
import requests
from typing import Dict, Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.location import Location
from config import Config


class LocationService:
    """Service for location detection and geocoding"""
    
    def __init__(self):
        """Initialize location service"""
        self.geolocator = Nominatim(user_agent="smart_weather_app")
        self.ipinfo_key = Config.IPINFO_API_KEY
    
    def get_location_by_ip(self) -> Optional[Dict]:
        """
        Detect user location using IP address
        
        Returns:
            Dictionary with location data or None if failed
        """
        try:
            # Use free ip-api.com (more reliable than ipinfo without key)
            response = requests.get("http://ip-api.com/json/", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Parse ip-api.com response
            if data.get('status') == 'success':
                return {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', ''),
                    'country': data.get('country', ''),
                    'latitude': data.get('lat', 0),
                    'longitude': data.get('lon', 0),
                    'timezone': data.get('timezone', ''),
                }
            else:
                print(f"IP geolocation failed: {data.get('message', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Failed to detect location by IP: {str(e)}")
            return None
    
    def get_coordinates_by_city(self, city: str, country: Optional[str] = None) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a city name
        
        Args:
            city: City name
            country: Country name or code (optional)
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            query = f"{city}, {country}" if country else city
            location = self.geolocator.geocode(query, timeout=10)  # type: ignore
            
            if location:
                return (location.latitude, location.longitude)  # type: ignore
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {str(e)}")
            return None
    
    def get_city_by_coordinates(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Reverse geocoding: Get city name from coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with location details or None
        """
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}", timeout=10)  # type: ignore
            
            if location and location.raw:  # type: ignore
                address = location.raw.get('address', {})  # type: ignore
                return {
                    'city': address.get('city') or address.get('town') or address.get('village', 'Unknown'),
                    'state': address.get('state', ''),
                    'country': address.get('country', ''),
                    'country_code': address.get('country_code', '').upper(),
                    'display_name': location.address,  # type: ignore
                    'latitude': lat,
                    'longitude': lon
                }
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Reverse geocoding error: {str(e)}")
            return None
    
    def search_locations(self, query: str, limit: int = 5) -> list:
        """
        Search for locations matching a query
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of location dictionaries
        """
        try:
            locations = self.geolocator.geocode(query, exactly_one=False, limit=limit, timeout=10)  # type: ignore
            
            if not locations:
                return []
            
            results = []
            for loc in locations:  # type: ignore
                results.append({
                    'display_name': loc.address,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'raw': loc.raw
                })
            
            return results
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Location search error: {str(e)}")
            return []
    
    def get_default_location(self) -> Dict:
        """
        Get a default location (fallback)
        
        Returns:
            Default location dictionary
        """
        # Default to New Delhi, India as a central location
        return {
            'city': 'New Delhi',
            'region': 'Delhi',
            'country': 'India',
            'latitude': 28.6139,
            'longitude': 77.2090,
            'timezone': 'Asia/Kolkata'
        }
