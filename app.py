"""
Smart Weather App - Flask Application
Main web application for agriculture and travel weather recommendations
"""
from flask import Flask, render_template, request, jsonify, session
from weather_service import WeatherService
from location_service import LocationService
from recommendations import RecommendationEngine
from visualizations import WeatherVisualizer
from config import Config
import traceback

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

# Initialize services
weather_service = WeatherService()
location_service = LocationService()
recommendation_engine = RecommendationEngine()
visualizer = WeatherVisualizer()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/agriculture')
def agriculture():
    """Agriculture mode page"""
    return render_template('agriculture.html')


@app.route('/travel')
def travel():
    """Travel mode page"""
    return render_template('travel.html')


@app.route('/test-charts')
def test_charts():
    """Test charts page"""
    return render_template('../test_charts.html')


@app.route('/api/location/auto')
def auto_detect_location():
    """Auto-detect user location by IP"""
    try:
        location = location_service.get_location_by_ip()
        if not location:
            location = location_service.get_default_location()
        
        return jsonify({
            'success': True,
            'location': location
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/location/search')
def search_location():
    """Search for locations"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter required'
        }), 400
    
    try:
        locations = location_service.search_locations(query)
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/weather/current')
def get_current_weather():
    """Get current weather for a location"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    try:
        if lat is not None and lon is not None:
            weather = weather_service.get_current_weather(lat, lon)
        elif city:
            weather = weather_service.get_weather_by_city(city)
        else:
            return jsonify({
                'success': False,
                'error': 'Either lat/lon or city parameter required'
            }), 400
        
        # Get location details if coordinates provided
        if lat is not None and lon is not None:
            location_info = location_service.get_city_by_coordinates(lat, lon)
            if location_info:
                weather['city'] = location_info['city']
                weather['country'] = location_info.get('country_code', weather.get('country', ''))
        
        return jsonify({
            'success': True,
            'weather': weather
        })
    except Exception as e:
        print(f"Error fetching weather: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/weather/forecast')
def get_forecast():
    """Get weather forecast"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    days = request.args.get('days', default=5, type=int)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': 'lat and lon parameters required'
        }), 400
    
    try:
        forecast = weather_service.get_forecast(lat, lon, days)
        return jsonify({
            'success': True,
            'forecast': forecast
        })
    except Exception as e:
        print(f"Error fetching forecast: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommendations/agriculture')
def get_agriculture_recommendations():
    """Get agriculture-specific recommendations"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': 'lat and lon parameters required'
        }), 400
    
    try:
        # Get current weather and forecast
        weather = weather_service.get_current_weather(lat, lon)
        forecast = weather_service.get_forecast(lat, lon, 5)
        
        # Generate recommendations
        recommendations = recommendation_engine.get_agriculture_recommendations(weather, forecast)
        
        return jsonify({
            'success': True,
            'weather': weather,
            'forecast': forecast,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error generating agriculture recommendations: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommendations/travel')
def get_travel_recommendations():
    """Get travel-specific recommendations"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': 'lat and lon parameters required'
        }), 400
    
    try:
        # Get current weather and forecast
        weather = weather_service.get_current_weather(lat, lon)
        forecast = weather_service.get_forecast(lat, lon, 5)
        
        # Generate recommendations
        recommendations = recommendation_engine.get_travel_recommendations(weather, forecast)
        
        return jsonify({
            'success': True,
            'weather': weather,
            'forecast': forecast,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error generating travel recommendations: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/visualizations/temperature')
def get_temperature_chart():
    """Get temperature chart"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': 'lat and lon parameters required'
        }), 400
    
    try:
        print(f"Fetching temperature chart for lat={lat}, lon={lon}")
        forecast = weather_service.get_forecast(lat, lon, 7)
        print(f"Got forecast with {len(forecast)} days")
        
        chart_html = visualizer.create_temperature_chart(forecast, format='html')
        print(f"Generated chart HTML, length: {len(chart_html)}")
        
        return jsonify({
            'success': True,
            'chart': chart_html
        })
    except Exception as e:
        print(f"Error creating temperature chart: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/visualizations/rainfall')
def get_rainfall_chart():
    """Get rainfall chart"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': 'lat and lon parameters required'
        }), 400
    
    try:
        print(f"Fetching rainfall chart for lat={lat}, lon={lon}")
        forecast = weather_service.get_forecast(lat, lon, 7)
        print(f"Got forecast with {len(forecast)} days")
        
        chart_html = visualizer.create_rainfall_chart(forecast, format='html')
        print(f"Generated chart HTML, length: {len(chart_html)}")
        
        return jsonify({
            'success': True,
            'chart': chart_html
        })
    except Exception as e:
        print(f"Error creating rainfall chart: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
