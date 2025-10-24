"""
Simple test script to verify the setup
"""
import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required = [
        'flask',
        'requests',
        'geopy',
        'matplotlib',
        'seaborn',
        'plotly',
        'pandas',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✓ {package} - installed")
        except ImportError:
            print(f"✗ {package} - missing")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\nChecking configuration...")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  Create .env file from .env.example and add your API key")
        return False
    
    print("✓ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    if not api_key or api_key == 'your_api_key_here':
        print("✗ OpenWeatherMap API key not configured")
        print("  Add your API key to .env file")
        return False
    
    print("✓ API key configured")
    return True

def test_api_connection():
    """Test connection to OpenWeatherMap API"""
    print("\nTesting API connection...")
    
    try:
        from weather_service import WeatherService
        service = WeatherService()
        
        # Test with New Delhi coordinates
        weather = service.get_current_weather(28.6139, 77.2090)
        
        if weather and 'temperature' in weather:
            print(f"✓ API connection successful")
            print(f"  Sample data: {weather['city']}, {weather['temperature']}°C")
            return True
        else:
            print("✗ Invalid response from API")
            return False
            
    except Exception as e:
        print(f"✗ API test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Smart Weather App - Setup Verification")
    print("=" * 50)
    
    tests = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
    ]
    
    if all(tests):
        print("\n" + "=" * 50)
        print("All basic checks passed!")
        print("Testing API connection...")
        print("=" * 50)
        test_api_connection()
    else:
        print("\n" + "=" * 50)
        print("Setup incomplete. Please fix the issues above.")
        print("=" * 50)
        return False
    
    print("\n" + "=" * 50)
    print("Setup verification complete!")
    print("Run 'python app.py' to start the application")
    print("=" * 50)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
