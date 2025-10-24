# Smart Weather App 🌤️

A Python-based Smart Weather Application that delivers real-time, location-specific weather data tailored for **Farmers** and **Travelers**.

## 🎯 Features

### Agriculture Mode 🌾
- **Crop-specific recommendations** based on weather conditions
- **Agricultural alerts** for frost, heat stress, and high winds
- **Irrigation recommendations** based on rainfall forecasts
- **Disease risk alerts** for high humidity conditions
- **Optimal farming activity suggestions** (spraying, harvesting, etc.)
- **Seasonal crop advice** and planting calendars

### Travel Mode ✈️
- **Smart packing lists** based on weather conditions
- **Route weather advisories** and safety alerts
- **Trip-aware forecasts** for destination planning
- **Best travel times** recommendations
- **Activity suggestions** based on weather outlook
- **Visibility and wind warnings** for safe travel

### General Features
- 📍 **Auto-location detection** via IP address
- 🗺️ **Manual location search** with geocoding
- 📊 **Interactive visualizations** (temperature, rainfall, humidity trends)
- 📈 **5-7 day weather forecasts**
- 🎨 **Mobile-responsive design**
- ⚡ **Real-time weather updates**

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **OpenWeatherMap API** - Weather data source
- **geopy** - Geocoding and location services
- **pandas** - Data processing

### Frontend
- **Bootstrap 5** - UI framework
- **Plotly** - Interactive charts
- **Matplotlib/Seaborn** - Static visualizations
- **JavaScript (ES6+)** - Client-side logic

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key (free tier available)

### Step 1: Clone or Download the Project
```bash
cd weather
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

   Get your free API key from: https://openweathermap.org/api

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🚀 Usage

### For Farmers (Agriculture Mode)
1. Navigate to **Agriculture Mode** from the home page
2. Allow auto-detection or search for your farm location
3. View current weather conditions and alerts
4. Check recommended farming activities for the day
5. Review 5-day forecast for planning
6. Follow irrigation and spraying recommendations

### For Travelers (Travel Mode)
1. Navigate to **Travel Mode** from the home page
2. Enter your destination or use current location
3. View travel outlook and weather alerts
4. Check the smart packing list
5. Review best times for outdoor activities
6. Plan your trip based on the forecast

## 📁 Project Structure

```
weather/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── weather_service.py          # Weather API integration
├── location_service.py         # Location detection & geocoding
├── recommendations.py          # Smart recommendation engine
├── visualizations.py           # Chart generation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── main.js            # Shared utilities
│       ├── agriculture.js     # Agriculture mode logic
│       └── travel.js          # Travel mode logic
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── agriculture.html       # Agriculture mode page
    └── travel.html            # Travel mode page
```

## 🔧 Configuration

### Weather Thresholds
Edit `config.py` to customize alert thresholds:

```python
AGRICULTURE_THRESHOLDS = {
    'wind_speed_spray': 20,    # km/h - max wind for spraying
    'rain_threshold': 10,      # mm - significant rainfall
    'frost_temp': 2,           # °C - frost warning
    'heat_stress': 35,         # °C - heat stress
    'high_humidity': 80,       # % - disease risk
}
```

### API Configuration
- Default API endpoint: OpenWeatherMap
- Update interval: Real-time (on-demand)
- Forecast range: 5 days (adjustable)

## 🌍 Real-World Impact

### For Agriculture
- ✅ **Reduced crop losses** through early frost/storm warnings
- ✅ **Optimized irrigation** saving water and costs
- ✅ **Better spray timing** improving pesticide effectiveness
- ✅ **Disease prevention** with humidity alerts
- ✅ **Improved yields** through data-driven decisions

### For Travel
- ✅ **Safer journeys** with weather-aware route planning
- ✅ **Better trip planning** avoiding bad weather days
- ✅ **Optimized packing** reducing over/under-packing
- ✅ **Enhanced experiences** with activity recommendations
- ✅ **Reduced disruptions** from weather-related delays

## 🔒 API Keys and Security

- **Never commit** your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Keep your API keys private
- Use environment variables for production deployment

## 🐛 Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: OpenWeatherMap API key is required
```
**Solution:** Add your API key to the `.env` file

**2. Location Detection Fails**
- Check internet connection
- Try manual location search instead
- Verify geopy is installed correctly

**3. Charts Not Loading**
- Ensure matplotlib and plotly are installed
- Check browser console for JavaScript errors
- Verify API endpoints are responding

## 📊 API Endpoints

### Location APIs
- `GET /api/location/auto` - Auto-detect location
- `GET /api/location/search?q=city` - Search locations

### Weather APIs
- `GET /api/weather/current?lat=X&lon=Y` - Current weather
- `GET /api/weather/forecast?lat=X&lon=Y` - Forecast

### Recommendation APIs
- `GET /api/recommendations/agriculture?lat=X&lon=Y` - Agriculture mode
- `GET /api/recommendations/travel?lat=X&lon=Y` - Travel mode

### Visualization APIs
- `GET /api/visualizations/temperature?lat=X&lon=Y` - Temperature chart
- `GET /api/visualizations/rainfall?lat=X&lon=Y` - Rainfall chart

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional weather data sources
- More crop-specific recommendations
- Multi-language support
- Mobile app version
- Historical weather analysis
- Machine learning predictions

## 📄 License

This project is open-source and available for educational and commercial use.

## 🙏 Acknowledgments

- **OpenWeatherMap** for weather data API
- **geopy** for geocoding services
- **Bootstrap** for UI components
- **Plotly** for interactive visualizations

## 📧 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check OpenWeatherMap API status

## 🔮 Future Enhancements

- [ ] Push notifications for severe weather
- [ ] Historical weather data analysis
- [ ] Crop yield prediction using ML
- [ ] Integration with IoT sensors
- [ ] Multi-day trip planning
- [ ] Collaborative travel groups
- [ ] Weather-based commodity price insights
- [ ] Offline mode with cached data

---

**Made with ❤️ for Farmers and Travelers**

**Version:** 1.0.0  
**Last Updated:** October 2025
