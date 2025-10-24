"""
Weather Data Visualization Module
Creates charts and graphs for weather data
"""
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for web apps
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List
import io
import base64
import pandas as pd


class WeatherVisualizer:
    """Class for creating weather visualizations"""
    
    def __init__(self):
        """Initialize visualizer with style settings"""
        # Set seaborn style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def create_temperature_chart(self, forecast: List[Dict], format='png') -> str:
        """
        Create temperature trend chart
        
        Args:
            forecast: List of forecast dictionaries
            format: 'png' for matplotlib or 'html' for plotly
            
        Returns:
            Base64 encoded image or HTML string
        """
        if format == 'html':
            return self._create_temperature_plotly(forecast)
        else:
            return self._create_temperature_matplotlib(forecast)
    
    def _create_temperature_matplotlib(self, forecast: List[Dict]) -> str:
        """Create temperature chart using matplotlib"""
        dates = [f['date'] for f in forecast]
        temp_max = [f['temp_max'] for f in forecast]
        temp_min = [f['temp_min'] for f in forecast]
        temp_avg = [f['temp_avg'] for f in forecast]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, temp_max, marker='o', label='Max Temp', color='#ff6b6b', linewidth=2)
        plt.plot(dates, temp_avg, marker='s', label='Avg Temp', color='#4ecdc4', linewidth=2)
        plt.plot(dates, temp_min, marker='^', label='Min Temp', color='#45b7d1', linewidth=2)
        
        plt.fill_between(dates, temp_min, temp_max, alpha=0.2, color='#4ecdc4')
        
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
        plt.title('Temperature Forecast', fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._fig_to_base64()
    
    def _create_temperature_plotly(self, forecast: List[Dict]) -> str:
        """Create interactive temperature chart using plotly"""
        if not forecast or len(forecast) == 0:
            return '<div class="alert alert-warning">No forecast data available</div>'
        
        dates = [f['date'].strftime('%Y-%m-%d') for f in forecast]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates, y=[f['temp_max'] for f in forecast],
            name='Max Temperature',
            mode='lines+markers',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, y=[f['temp_avg'] for f in forecast],
            name='Avg Temperature',
            mode='lines+markers',
            line=dict(color='#4ecdc4', width=3),
            marker=dict(size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, y=[f['temp_min'] for f in forecast],
            name='Min Temperature',
            mode='lines+markers',
            line=dict(color='#45b7d1', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title=dict(text='Temperature Forecast', font=dict(size=20)),
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            hovermode='x unified',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Use 'cdn' to include Plotly from CDN for reliability
        config = {'displayModeBar': True, 'responsive': True}
        html = fig.to_html(
            full_html=False, 
            include_plotlyjs='cdn',
            div_id='temp-chart',
            config=config
        )
        return html
    
    def create_rainfall_chart(self, forecast: List[Dict], format='png') -> str:
        """Create rainfall comparison chart"""
        if format == 'html':
            return self._create_rainfall_plotly(forecast)
        else:
            return self._create_rainfall_matplotlib(forecast)
    
    def _create_rainfall_matplotlib(self, forecast: List[Dict]) -> str:
        """Create rainfall bar chart using matplotlib"""
        dates = [f['date'].strftime('%m/%d') for f in forecast]
        rainfall = [f['total_rain'] for f in forecast]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(dates, rainfall, color='#45b7d1', alpha=0.7, edgecolor='#2c3e50')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}mm',
                        ha='center', va='bottom', fontsize=9)
        
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Rainfall (mm)', fontsize=12, fontweight='bold')
        plt.title('Rainfall Forecast', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return self._fig_to_base64()
    
    def _create_rainfall_plotly(self, forecast: List[Dict]) -> str:
        """Create interactive rainfall chart using plotly"""
        if not forecast or len(forecast) == 0:
            return '<div class="alert alert-warning">No forecast data available</div>'
        
        dates = [f['date'].strftime('%Y-%m-%d') for f in forecast]
        rainfall = [f['total_rain'] for f in forecast]
        
        fig = go.Figure(data=[
            go.Bar(
                x=dates,
                y=rainfall,
                marker_color='#45b7d1',
                text=[f'{r:.1f}mm' if r > 0 else '' for r in rainfall],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=dict(text='Rainfall Forecast', font=dict(size=20)),
            xaxis_title='Date',
            yaxis_title='Rainfall (mm)',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Use 'cdn' to include Plotly from CDN for reliability
        config = {'displayModeBar': True, 'responsive': True}
        html = fig.to_html(
            full_html=False,
            include_plotlyjs='cdn',
            div_id='rain-chart',
            config=config
        )
        return html
    
    def create_humidity_wind_chart(self, forecast: List[Dict], format='png') -> str:
        """Create combined humidity and wind speed chart"""
        if format == 'html':
            return self._create_humidity_wind_plotly(forecast)
        else:
            return self._create_humidity_wind_matplotlib(forecast)
    
    def _create_humidity_wind_matplotlib(self, forecast: List[Dict]) -> str:
        """Create dual-axis chart for humidity and wind"""
        dates = [f['date'].strftime('%m/%d') for f in forecast]
        humidity = [f['humidity_avg'] for f in forecast]
        wind = [f['wind_speed_max'] for f in forecast]
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        color1 = '#4ecdc4'
        ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Humidity (%)', color=color1, fontsize=12, fontweight='bold')
        ax1.plot(dates, humidity, marker='o', color=color1, linewidth=2, label='Humidity')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, alpha=0.3)
        
        ax2 = ax1.twinx()
        color2 = '#ff6b6b'
        ax2.set_ylabel('Wind Speed (km/h)', color=color2, fontsize=12, fontweight='bold')
        ax2.plot(dates, wind, marker='s', color=color2, linewidth=2, label='Wind Speed')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        plt.title('Humidity and Wind Speed Forecast', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        fig.tight_layout()
        
        return self._fig_to_base64()
    
    def _create_humidity_wind_plotly(self, forecast: List[Dict]) -> str:
        """Create interactive dual-axis chart using plotly"""
        dates = [f['date'].strftime('%Y-%m-%d') for f in forecast]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=[f['humidity_avg'] for f in forecast],
            name='Humidity',
            yaxis='y',
            mode='lines+markers',
            line=dict(color='#4ecdc4', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=[f['wind_speed_max'] for f in forecast],
            name='Wind Speed',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#ff6b6b', width=3)
        ))
        
        fig.update_layout(
            title='Humidity and Wind Speed Forecast',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Humidity (%)', side='left'),
            yaxis2=dict(title='Wind Speed (km/h)', side='right', overlaying='y'),
            hovermode='x unified',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Return HTML without including plotlyjs (loaded globally in base.html)
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_weather_summary_card(self, weather_data: Dict) -> Dict:
        """
        Create data for weather summary card
        
        Args:
            weather_data: Current weather data
            
        Returns:
            Dictionary with formatted weather info
        """
        return {
            'temperature': f"{weather_data['temperature']:.1f}°C",
            'feels_like': f"{weather_data['feels_like']:.1f}°C",
            'description': weather_data['description'].title(),
            'humidity': f"{weather_data['humidity']}%",
            'wind_speed': f"{weather_data['wind_speed']:.1f} km/h",
            'pressure': f"{weather_data['pressure']} hPa",
            'visibility': f"{weather_data['visibility']:.1f} km",
            'icon': weather_data['icon'],
            'city': weather_data['city'],
            'country': weather_data['country']
        }
    
    def _fig_to_base64(self) -> str:
        """Convert matplotlib figure to base64 encoded string"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        return f"data:image/png;base64,{image_base64}"
    
    def create_forecast_table(self, forecast: List[Dict]) -> pd.DataFrame:
        """
        Create a pandas DataFrame from forecast data
        
        Args:
            forecast: List of forecast dictionaries
            
        Returns:
            DataFrame with formatted forecast data
        """
        data = []
        for f in forecast:
            data.append({
                'Date': f['date'].strftime('%Y-%m-%d'),
                'Min Temp (°C)': f'{f["temp_min"]:.1f}',
                'Max Temp (°C)': f'{f["temp_max"]:.1f}',
                'Avg Temp (°C)': f'{f["temp_avg"]:.1f}',
                'Rainfall (mm)': f'{f["total_rain"]:.1f}',
                'Humidity (%)': f'{f["humidity_avg"]:.1f}',
                'Max Wind (km/h)': f'{f["wind_speed_max"]:.1f}',
                'Conditions': f['description'].title()
            })
        
        return pd.DataFrame(data)
