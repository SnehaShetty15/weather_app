"""
Demo Script - Smart Weather App
Demonstrates the core functionality without running the web server
"""
from weather_service import WeatherService
from location_service import LocationService
from recommendations import RecommendationEngine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def demo_agriculture_mode():
    """Demonstrate agriculture mode"""
    print_section("AGRICULTURE MODE DEMO")
    
    try:
        # Initialize services
        weather_service = WeatherService()
        recommendation_engine = RecommendationEngine()
        
        # Use sample location: Punjab, India (agriculture region)
        lat, lon = 30.7333, 76.7794
        city = "Chandigarh, Punjab"
        
        print(f"\nLocation: {city}")
        print(f"Coordinates: {lat}, {lon}")
        
        # Get current weather
        print("\n📊 Fetching current weather...")
        weather = weather_service.get_current_weather(lat, lon)
        
        print(f"\n🌡️  Temperature: {weather['temperature']:.1f}°C")
        print(f"💨 Wind Speed: {weather['wind_speed']:.1f} km/h")
        print(f"💧 Humidity: {weather['humidity']}%")
        print(f"☁️  Conditions: {weather['description'].title()}")
        
        # Get forecast
        print("\n📅 Fetching 5-day forecast...")
        forecast = weather_service.get_forecast(lat, lon, 5)
        
        # Generate agriculture recommendations
        print("\n🌾 Generating Agriculture Recommendations...")
        recommendations = recommendation_engine.get_agriculture_recommendations(weather, forecast)
        
        # Display alerts
        if recommendations['alerts']:
            print("\n⚠️  WEATHER ALERTS:")
            for alert in recommendations['alerts']:
                print(f"  • [{alert['severity'].upper()}] {alert['title']}")
                print(f"    {alert['message']}")
        else:
            print("\n✅ No weather alerts")
        
        # Display recommendations
        if recommendations['recommendations']:
            print("\n💡 RECOMMENDATIONS:")
            for rec in recommendations['recommendations']:
                print(f"  • {rec}")
        
        # Display tasks
        if recommendations['tasks']:
            print("\n📋 TODAY'S TASKS:")
            for task in recommendations['tasks']:
                print(f"  • {task}")
        
        # Display suitable activities
        if recommendations['suitable_activities']:
            print("\n✅ SUITABLE FARM ACTIVITIES:")
            for activity in recommendations['suitable_activities']:
                print(f"  • {activity}")
        
        # Display forecast summary
        print("\n📆 5-DAY FORECAST:")
        for day in forecast:
            date_str = day['date'].strftime('%a, %b %d')
            print(f"  {date_str}: {day['temp_min']:.0f}-{day['temp_max']:.0f}°C, "
                  f"{day['description'].title()}, "
                  f"Rain: {day['total_rain']:.1f}mm")
        
        print("\n✅ Agriculture Mode Demo Complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have set your OPENWEATHER_API_KEY in .env file")

def demo_travel_mode():
    """Demonstrate travel mode"""
    print_section("TRAVEL MODE DEMO")
    
    try:
        # Initialize services
        weather_service = WeatherService()
        recommendation_engine = RecommendationEngine()
        
        # Use sample location: Paris, France (tourist destination)
        lat, lon = 48.8566, 2.3522
        city = "Paris, France"
        
        print(f"\nDestination: {city}")
        print(f"Coordinates: {lat}, {lon}")
        
        # Get current weather
        print("\n📊 Fetching current weather...")
        weather = weather_service.get_current_weather(lat, lon)
        
        print(f"\n🌡️  Temperature: {weather['temperature']:.1f}°C")
        print(f"🤔 Feels Like: {weather['feels_like']:.1f}°C")
        print(f"💨 Wind Speed: {weather['wind_speed']:.1f} km/h")
        print(f"👁️  Visibility: {weather['visibility']:.1f} km")
        print(f"☁️  Conditions: {weather['description'].title()}")
        
        # Get forecast
        print("\n📅 Fetching 5-day forecast...")
        forecast = weather_service.get_forecast(lat, lon, 5)
        
        # Generate travel recommendations
        print("\n✈️  Generating Travel Recommendations...")
        recommendations = recommendation_engine.get_travel_recommendations(weather, forecast)
        
        # Display travel outlook
        print(f"\n🎯 TRAVEL OUTLOOK: {recommendations['travel_outlook'].upper()}")
        
        # Display alerts
        if recommendations['alerts']:
            print("\n⚠️  WEATHER ALERTS:")
            for alert in recommendations['alerts']:
                print(f"  • {alert['title']}")
                print(f"    {alert['message']}")
        else:
            print("\n✅ No weather alerts - safe to travel!")
        
        # Display packing list
        if recommendations['packing_list']:
            print("\n🎒 SMART PACKING LIST:")
            for item in recommendations['packing_list']:
                print(f"  • {item}")
        
        # Display recommendations
        if recommendations['recommendations']:
            print("\n💡 TRAVEL TIPS:")
            for rec in recommendations['recommendations']:
                print(f"  • {rec}")
        
        # Display best times
        if recommendations['best_times']:
            print("\n⏰ BEST TIMES FOR ACTIVITIES:")
            for time in recommendations['best_times']:
                print(f"  • {time}")
        
        # Display forecast summary
        print("\n📆 5-DAY FORECAST:")
        for day in forecast:
            date_str = day['date'].strftime('%a, %b %d')
            outlook = "Good" if day['total_rain'] < 5 else "Rainy"
            print(f"  {date_str}: {day['temp_min']:.0f}-{day['temp_max']:.0f}°C, "
                  f"{day['description'].title()} - {outlook} for sightseeing")
        
        print("\n✅ Travel Mode Demo Complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have set your OPENWEATHER_API_KEY in .env file")

def demo_location_service():
    """Demonstrate location service"""
    print_section("LOCATION SERVICE DEMO")
    
    try:
        location_service = LocationService()
        
        # Auto-detect location
        print("\n🌍 Auto-detecting your location...")
        location = location_service.get_location_by_ip()
        
        if location:
            print(f"\n📍 Detected Location:")
            print(f"  City: {location['city']}")
            print(f"  Region: {location['region']}")
            print(f"  Country: {location['country']}")
            print(f"  Coordinates: {location['latitude']}, {location['longitude']}")
        else:
            print("\n⚠️  Auto-detection failed, using default location")
            location = location_service.get_default_location()
            print(f"  Default: {location['city']}, {location['country']}")
        
        # Search for a city
        print("\n🔍 Searching for 'London'...")
        results = location_service.search_locations("London", limit=3)
        
        if results:
            print(f"\n📍 Found {len(results)} location(s):")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['display_name']}")
        
        print("\n✅ Location Service Demo Complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main():
    """Run all demos"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "SMART WEATHER APP - DEMO SCRIPT" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Check if API key is configured
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    if not api_key or api_key == 'your_api_key_here':
        print("\n❌ ERROR: OpenWeatherMap API key not configured!")
        print("\n📝 Please follow these steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Get your free API key from https://openweathermap.org/api")
        print("  3. Add your API key to the .env file")
        print("  4. Run this demo again\n")
        return
    
    print("\nThis demo will showcase the Smart Weather App's core features")
    print("without running the web interface.\n")
    
    # Run demos
    demos = [
        ("Location Service", demo_location_service),
        ("Agriculture Mode", demo_agriculture_mode),
        ("Travel Mode", demo_travel_mode),
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n\n⏹️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ {name} demo failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)
    print("\n💻 To use the web interface, run: python app.py")
    print("🌐 Then open: http://localhost:5000\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user. Goodbye! 👋")
