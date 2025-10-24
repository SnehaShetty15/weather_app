# Quick Start Guide - Smart Weather App

## 🚀 Get Started in 5 Minutes!

### Step 1: Get Your API Key (2 minutes)
1. Go to https://openweathermap.org/api
2. Click "Sign Up" (it's FREE!)
3. After signing up, go to your account → API Keys
4. Copy your API key

### Step 2: Setup Environment (1 minute)
1. Open the project folder in your terminal/command prompt
2. Create a `.env` file:
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux use: `cp .env.example .env`)

3. Open `.env` in a text editor and replace `your_api_key_here` with your actual API key:
   ```
   OPENWEATHER_API_KEY=abc123your_actual_key_here
   ```

### Step 3: Install Dependencies (1 minute)
```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 4: Test Setup (30 seconds)
```bash
python test_setup.py
```

This will verify everything is working correctly.

### Step 5: Run the App! (30 seconds)
```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

🎉 **That's it! You're ready to use the Smart Weather App!**

---

## 📱 Using the App

### For Farmers:
1. Click **"Agriculture Mode"**
2. Allow location detection or enter your farm location
3. View alerts, recommendations, and forecasts
4. Check suitable farming activities for today

### For Travelers:
1. Click **"Travel Mode"**
2. Enter your destination
3. View packing list and travel recommendations
4. Check weather forecast for trip planning

---

## ⚠️ Troubleshooting

**Problem:** Can't install packages
```bash
# Try upgrading pip first
python -m pip install --upgrade pip
# Then retry
pip install -r requirements.txt
```

**Problem:** API key error
- Make sure you copied the entire API key
- No spaces before or after the key in .env file
- Wait 10-15 minutes after creating account (activation time)

**Problem:** Location detection not working
- Try manual search instead
- Check your internet connection

**Problem:** Port 5000 already in use
Edit `app.py` and change the port:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Changed to 8080
```

---

## 🎯 Next Steps

- Explore both Agriculture and Travel modes
- Try different locations
- Check the interactive charts
- Review 5-day forecasts
- Customize thresholds in `config.py`

---

## 📞 Need Help?

1. Check README.md for detailed documentation
2. Review the troubleshooting section above
3. Verify your API key is active at https://home.openweathermap.org/api_keys

**Happy Weather Tracking! 🌤️**
