"""
Smart Recommendations Engine
Provides agriculture and travel-specific recommendations
"""
from typing import Dict, List, Optional
from datetime import datetime, date
from config import Config


class RecommendationEngine:
    """Engine for generating smart weather-based recommendations"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.ag_thresholds = Config.AGRICULTURE_THRESHOLDS
        self.travel_thresholds = Config.TRAVEL_THRESHOLDS
    
    def get_agriculture_recommendations(self, weather_data: Dict, forecast: Optional[List[Dict]] = None) -> Dict:
        """
        Generate agriculture-specific recommendations
        
        Args:
            weather_data: Current weather data
            forecast: Optional forecast data for next few days
            
        Returns:
            Dictionary with recommendations and alerts
        """
        recommendations = []
        alerts = []
        tasks = []
        
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        humidity = weather_data['humidity']
        rain = weather_data.get('rain_1h', 0) + weather_data.get('rain_3h', 0)
        
        # Wind-related recommendations
        if wind_speed > self.ag_thresholds['wind_speed_spray']:
            alerts.append({
                'type': 'warning',
                'title': '⚠️ High Wind Alert',
                'message': f'Wind speed is {wind_speed:.1f} km/h. Avoid pesticide/fertilizer spraying.',
                'severity': 'high'
            })
            tasks.append('Postpone spraying operations until wind subsides')
        else:
            tasks.append('✓ Good conditions for spraying operations')
        
        # Temperature-related recommendations
        if temp <= self.ag_thresholds['frost_temp']:
            alerts.append({
                'type': 'danger',
                'title': '❄️ Frost Warning',
                'message': f'Temperature is {temp:.1f}°C. Protect sensitive crops from frost damage.',
                'severity': 'critical'
            })
            tasks.append('Cover sensitive crops or use frost protection methods')
        elif temp >= self.ag_thresholds['heat_stress']:
            alerts.append({
                'type': 'warning',
                'title': '🌡️ Heat Stress Alert',
                'message': f'High temperature {temp:.1f}°C may stress crops. Ensure adequate irrigation.',
                'severity': 'high'
            })
            tasks.append('Increase irrigation frequency')
        
        # Rainfall recommendations
        if rain > self.ag_thresholds['rain_threshold']:
            recommendations.append(f'Heavy rainfall detected ({rain:.1f}mm). Delay irrigation.')
            tasks.append('Skip irrigation today - sufficient rainfall')
        elif rain > 0:
            recommendations.append(f'Light rainfall ({rain:.1f}mm) expected. Monitor soil moisture.')
        else:
            # Check forecast for rain
            if forecast:
                upcoming_rain = sum(f['total_rain'] for f in forecast[:3])
                if upcoming_rain > 5:
                    recommendations.append(f'Rain expected in next 3 days ({upcoming_rain:.1f}mm). Plan irrigation accordingly.')
                else:
                    tasks.append('Regular irrigation recommended')
        
        # Humidity recommendations
        if humidity >= self.ag_thresholds['high_humidity']:
            alerts.append({
                'type': 'info',
                'title': '💧 High Humidity Alert',
                'message': f'Humidity at {humidity}%. Increased risk of fungal diseases.',
                'severity': 'medium'
            })
            recommendations.append('Monitor crops for signs of fungal infection')
            tasks.append('Apply preventive fungicide if needed')
        
        # Seasonal crop recommendations
        current_season = self._get_season()
        crop_advice = self._get_crop_advice(current_season, weather_data)
        recommendations.extend(crop_advice)
        
        return {
            'alerts': alerts,
            'recommendations': recommendations,
            'tasks': tasks,
            'suitable_activities': self._get_suitable_farm_activities(weather_data),
            'crop_advice': crop_advice
        }
    
    def get_travel_recommendations(self, weather_data: Dict, forecast: Optional[List[Dict]] = None) -> Dict:
        """
        Generate travel-specific recommendations
        
        Args:
            weather_data: Current weather data
            forecast: Optional forecast data
            
        Returns:
            Dictionary with travel recommendations
        """
        recommendations = []
        alerts = []
        packing_list = []
        
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        rain = weather_data.get('rain_1h', 0) + weather_data.get('rain_3h', 0)
        description = weather_data.get('main', '').lower()
        
        # Temperature-based packing
        if temp <= self.travel_thresholds['cold_weather']:
            packing_list.extend(['Warm jacket', 'Gloves', 'Scarf', 'Thermal wear'])
            recommendations.append(f'Cold weather ({temp:.1f}°C). Pack warm clothing.')
        elif temp >= self.travel_thresholds['hot_weather']:
            packing_list.extend(['Sunscreen', 'Hat', 'Sunglasses', 'Light clothing', 'Water bottle'])
            recommendations.append(f'Hot weather ({temp:.1f}°C). Stay hydrated and use sun protection.')
        else:
            packing_list.extend(['Light jacket', 'Comfortable clothing'])
        
        # Rain recommendations
        if rain > self.travel_thresholds['rain_warning'] or 'rain' in description:
            alerts.append({
                'type': 'warning',
                'title': '☔ Rain Expected',
                'message': 'Pack rain gear and plan indoor activities.',
                'severity': 'medium'
            })
            packing_list.extend(['Umbrella', 'Raincoat', 'Waterproof bag'])
            recommendations.append('Consider indoor attractions or activities')
        
        # Wind warnings
        if wind_speed > self.travel_thresholds['wind_warning']:
            alerts.append({
                'type': 'warning',
                'title': '💨 Strong Winds',
                'message': f'Wind speed {wind_speed:.1f} km/h. Be cautious outdoors.',
                'severity': 'high'
            })
            recommendations.append('Avoid outdoor activities in exposed areas')
        
        # Weather condition recommendations
        if 'clear' in description or 'sun' in description:
            recommendations.append('Perfect weather for sightseeing and outdoor activities!')
        elif 'storm' in description or 'thunder' in description:
            alerts.append({
                'type': 'danger',
                'title': '⛈️ Storm Warning',
                'message': 'Severe weather expected. Stay indoors if possible.',
                'severity': 'critical'
            })
            recommendations.append('Postpone outdoor plans. Seek shelter.')
        elif 'fog' in description or 'mist' in description:
            alerts.append({
                'type': 'info',
                'title': '🌫️ Poor Visibility',
                'message': 'Fog/mist conditions. Drive carefully.',
                'severity': 'medium'
            })
            recommendations.append('Exercise caution while driving. Allow extra travel time.')
        
        # Forecast-based recommendations
        travel_outlook = 'good'
        if forecast:
            forecast_summary = self._analyze_forecast_for_travel(forecast)
            recommendations.append(forecast_summary['summary'])
            travel_outlook = forecast_summary['outlook']
        
        return {
            'alerts': alerts,
            'recommendations': recommendations,
            'packing_list': packing_list,
            'travel_outlook': travel_outlook,
            'best_times': self._get_best_travel_times(weather_data, forecast)
        }
    
    def _get_season(self) -> str:
        """Determine current season based on month"""
        month = datetime.now().month
        
        # Northern Hemisphere seasons
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def _get_crop_advice(self, season: str, weather_data: Dict) -> List[str]:
        """Get seasonal crop advice"""
        advice = []
        
        crop_calendar = {
            'spring': [
                'Good time for planting summer crops like corn, cotton, and vegetables',
                'Prepare soil with organic matter',
                'Monitor for late frost warnings'
            ],
            'summer': [
                'Focus on irrigation management',
                'Monitor for heat stress in crops',
                'Good time for harvesting wheat and early crops'
            ],
            'autumn': [
                'Plant winter crops like wheat, barley',
                'Harvest summer crops',
                'Prepare fields for winter'
            ],
            'winter': [
                'Protect crops from frost',
                'Plan for spring planting',
                'Maintain irrigation systems'
            ]
        }
        
        return crop_calendar.get(season, [])
    
    def _get_suitable_farm_activities(self, weather_data: Dict) -> List[str]:
        """Determine suitable farming activities for current weather"""
        activities = []
        
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        rain = weather_data.get('rain_1h', 0)
        
        if rain < 1 and wind_speed < 20 and 10 <= temp <= 30:
            activities.extend([
                'Pesticide/fertilizer application',
                'Harvesting',
                'Field preparation',
                'Planting',
                'Equipment maintenance'
            ])
        elif rain < 1 and wind_speed < 20:
            activities.extend([
                'Harvesting (if crops are ready)',
                'Equipment maintenance',
                'Storage management'
            ])
        elif rain >= 1:
            activities.extend([
                'Indoor activities only',
                'Planning and paperwork',
                'Equipment cleaning and maintenance'
            ])
        
        return activities
    
    def _analyze_forecast_for_travel(self, forecast: List[Dict]) -> Dict:
        """Analyze forecast for travel planning"""
        if not forecast:
            return {'summary': 'No forecast data available', 'outlook': 'unknown'}
        
        total_rain = sum(f['total_rain'] for f in forecast)
        avg_temp = sum(f['temp_avg'] for f in forecast) / len(forecast)
        max_wind = max(f['wind_speed_max'] for f in forecast)
        
        if total_rain > 20 or max_wind > 50:
            return {
                'summary': 'Challenging weather ahead. Consider rescheduling outdoor activities.',
                'outlook': 'poor'
            }
        elif total_rain < 5 and 15 <= avg_temp <= 28:
            return {
                'summary': 'Excellent weather forecast for the next few days!',
                'outlook': 'excellent'
            }
        else:
            return {
                'summary': 'Fair weather expected. Pack accordingly.',
                'outlook': 'fair'
            }
    
    def _get_best_travel_times(self, weather_data: Dict, forecast: Optional[List[Dict]]) -> List[str]:
        """Suggest best times for travel/outdoor activities"""
        suggestions = []
        
        sunrise = weather_data.get('sunrise')
        sunset = weather_data.get('sunset')
        
        if sunrise:
            suggestions.append(f'Sunrise at {sunrise.strftime("%H:%M")} - Great for photography')
        if sunset:
            suggestions.append(f'Sunset at {sunset.strftime("%H:%M")} - Beautiful evening views')
        
        # Suggest based on temperature
        temp = weather_data['temperature']
        if temp > 30:
            suggestions.append('Visit outdoor attractions early morning or late evening to avoid heat')
        elif temp < 10:
            suggestions.append('Midday (11 AM - 3 PM) will be warmest for outdoor activities')
        
        return suggestions
