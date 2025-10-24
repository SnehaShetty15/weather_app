// Agriculture Mode JavaScript

let currentLocation = null;

// Auto-detect location
document.getElementById('autoDetectBtn')?.addEventListener('click', async () => {
    Utils.showLoading();
    try {
        const response = await fetch('/api/location/auto');
        const data = await response.json();
        
        if (data.success) {
            currentLocation = data.location;
            updateLocationDisplay();
            loadWeatherData();
        } else {
            Utils.showError(data.error || 'Failed to detect location');
            Utils.hideLoading();
        }
    } catch (error) {
        Utils.showError('Network error: ' + error.message);
        Utils.hideLoading();
    }
});

// Search location
document.getElementById('searchBtn')?.addEventListener('click', async () => {
    const query = document.getElementById('locationSearch')?.value;
    if (!query) return;
    
    try {
        const response = await fetch(`/api/location/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.locations.length > 0) {
            displayLocationResults(data.locations);
        } else {
            Utils.showError('No locations found');
        }
    } catch (error) {
        Utils.showError('Search failed: ' + error.message);
    }
});

// Display location search results
function displayLocationResults(locations) {
    const container = document.getElementById('locationResults');
    if (!container) return;
    
    container.innerHTML = '';
    locations.forEach(loc => {
        const div = document.createElement('div');
        div.className = 'location-result';
        div.innerHTML = `<i class="bi bi-geo-alt"></i> ${loc.display_name}`;
        div.onclick = () => {
            currentLocation = {
                city: loc.display_name.split(',')[0],
                latitude: loc.latitude,
                longitude: loc.longitude
            };
            updateLocationDisplay();
            container.innerHTML = '';
            loadWeatherData();
        };
        container.appendChild(div);
    });
}

// Update location display
function updateLocationDisplay() {
    const card = document.getElementById('currentLocationCard');
    const text = document.getElementById('currentLocationText');
    if (card && text && currentLocation) {
        card.style.display = 'block';
        text.querySelector('span').textContent = currentLocation.city;
    }
}

// Load weather data
async function loadWeatherData() {
    if (!currentLocation) return;
    
    Utils.showLoading();
    
    try {
        const response = await fetch(
            `/api/recommendations/agriculture?lat=${currentLocation.latitude}&lon=${currentLocation.longitude}`
        );
        const data = await response.json();
        
        if (data.success) {
            displayWeatherData(data.weather);
            displayAlerts(data.recommendations.alerts);
            displayRecommendations(data.recommendations);
            displayForecast(data.forecast);
            loadCharts();
        } else {
            Utils.showError(data.error || 'Failed to load weather data');
        }
    } catch (error) {
        Utils.showError('Failed to load data: ' + error.message);
    } finally {
        Utils.hideLoading();
    }
}

// Display current weather
function displayWeatherData(weather) {
    document.getElementById('weatherIcon').src = Utils.getWeatherIcon(weather.icon);
    document.getElementById('temperature').textContent = `${Math.round(weather.temperature)}°C`;
    document.getElementById('weatherDescription').textContent = weather.description;
    document.getElementById('feelsLike').textContent = `${Math.round(weather.feels_like)}°C`;
    document.getElementById('humidity').textContent = `${weather.humidity}%`;
    document.getElementById('windSpeed').textContent = `${Math.round(weather.wind_speed)} km/h`;
    document.getElementById('pressure').textContent = `${weather.pressure} hPa`;
}

// Display alerts
function displayAlerts(alerts) {
    const container = document.getElementById('alertsContainer');
    if (!container) return;
    
    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<p class="text-muted">No alerts at this time ✓</p>';
        return;
    }
    
    container.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.severity}">
            <h6>${alert.title}</h6>
            <p class="mb-0">${alert.message}</p>
        </div>
    `).join('');
}

// Display recommendations
function displayRecommendations(recommendations) {
    // Recommendations list
    const recContainer = document.getElementById('recommendationsContainer');
    if (recContainer) {
        if (recommendations.recommendations && recommendations.recommendations.length > 0) {
            recContainer.innerHTML = '<ul class="list-group list-group-flush">' +
                recommendations.recommendations.map(rec => 
                    `<li class="list-group-item"><i class="bi bi-check-circle text-success"></i> ${rec}</li>`
                ).join('') + '</ul>';
        } else {
            recContainer.innerHTML = '<p class="text-muted">No specific recommendations</p>';
        }
    }
    
    // Tasks list
    const tasksContainer = document.getElementById('tasksContainer');
    if (tasksContainer) {
        if (recommendations.tasks && recommendations.tasks.length > 0) {
            tasksContainer.innerHTML = '<ul class="list-group list-group-flush">' +
                recommendations.tasks.map(task => 
                    `<li class="list-group-item">${task}</li>`
                ).join('') + '</ul>';
        } else {
            tasksContainer.innerHTML = '<p class="text-muted">No tasks for today</p>';
        }
    }
    
    // Suitable activities
    const activitiesContainer = document.getElementById('activitiesContainer');
    if (activitiesContainer) {
        if (recommendations.suitable_activities && recommendations.suitable_activities.length > 0) {
            activitiesContainer.innerHTML = '<ul class="list-group list-group-flush">' +
                recommendations.suitable_activities.map(activity => 
                    `<li class="list-group-item"><i class="bi bi-check text-success"></i> ${activity}</li>`
                ).join('') + '</ul>';
        } else {
            activitiesContainer.innerHTML = '<p class="text-muted">Limited outdoor activities recommended</p>';
        }
    }
}

// Display forecast table
function displayForecast(forecast) {
    const tbody = document.querySelector('#forecastTable tbody');
    if (!tbody) return;
    
    tbody.innerHTML = forecast.map(day => `
        <tr>
            <td>${Utils.formatDate(day.date)}</td>
            <td>
                <img src="${Utils.getWeatherIcon(day.icon)}" alt="${day.description}" style="width: 30px;">
                ${day.description}
            </td>
            <td>${Math.round(day.temp_min)}°C</td>
            <td>${Math.round(day.temp_max)}°C</td>
            <td>${day.total_rain > 0 ? day.total_rain.toFixed(1) + ' mm' : 'No rain'}</td>
            <td>${Math.round(day.wind_speed_max)} km/h</td>
        </tr>
    `).join('');
}

// Load charts
async function loadCharts() {
    if (!currentLocation) {
        console.error('No location available for charts');
        return;
    }
    
    console.log('Starting to load charts for location:', currentLocation);
    
    try {
        // Load temperature chart
        console.log('Loading temperature chart...');
        const tempResponse = await fetch(
            `/api/visualizations/temperature?lat=${currentLocation.latitude}&lon=${currentLocation.longitude}`
        );
        const tempData = await tempResponse.json();
        console.log('Temperature chart response:', tempData);
        
        if (tempData.success) {
            const chartContainer = document.getElementById('temperatureChart');
            if (chartContainer) {
                // Clear the container first
                chartContainer.innerHTML = '';
                
                // Create a temporary div to hold the HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = tempData.chart;
                
                // Append all scripts and content
                const scripts = tempDiv.querySelectorAll('script');
                const chartDiv = tempDiv.querySelector('.plotly-graph-div');
                
                if (chartDiv) {
                    chartContainer.appendChild(chartDiv);
                    
                    // Execute each script
                    scripts.forEach((script) => {
                        const newScript = document.createElement('script');
                        if (script.src) {
                            newScript.src = script.src;
                        } else {
                            newScript.textContent = script.textContent;
                        }
                        document.head.appendChild(newScript);
                        setTimeout(() => document.head.removeChild(newScript), 1000);
                    });
                    
                    console.log('✅ Temperature chart loaded successfully');
                    console.log('Chart HTML length:', tempData.chart.length);
                } else {
                    // Fallback: just insert the HTML
                    chartContainer.innerHTML = tempData.chart;
                    console.log('⚠️ Using fallback method');
                }
                
                setTimeout(() => {
                    const plotlyDiv = chartContainer.querySelector('.plotly-graph-div');
                    if (plotlyDiv) {
                        console.log('✅ Plotly div found:', plotlyDiv.id);
                        console.log('Plotly div dimensions:', plotlyDiv.offsetWidth, 'x', plotlyDiv.offsetHeight);
                    } else {
                        console.error('❌ Plotly div not found');
                    }
                }, 1000);
            } else {
                console.error('❌ Temperature chart container not found');
            }
        } else {
            console.error('❌ Temperature chart error:', tempData.error);
            const container = document.getElementById('temperatureChart');
            if (container) {
                container.innerHTML = 
                    `<div class="alert alert-warning">Failed to load temperature chart: ${tempData.error || 'Unknown error'}</div>`;
            }
        }
        
        // Small delay to ensure first chart renders
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Load rainfall chart
        console.log('Loading rainfall chart...');
        const rainResponse = await fetch(
            `/api/visualizations/rainfall?lat=${currentLocation.latitude}&lon=${currentLocation.longitude}`
        );
        const rainData = await rainResponse.json();
        console.log('Rainfall chart response:', rainData);
        
        if (rainData.success) {
            const chartContainer = document.getElementById('rainfallChart');
            if (chartContainer) {
                // Clear the container first
                chartContainer.innerHTML = '';
                
                // Create a temporary div to hold the HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = rainData.chart;
                
                // Append all scripts and content
                const scripts = tempDiv.querySelectorAll('script');
                const chartDiv = tempDiv.querySelector('.plotly-graph-div');
                
                if (chartDiv) {
                    chartContainer.appendChild(chartDiv);
                    
                    // Execute each script
                    scripts.forEach((script) => {
                        const newScript = document.createElement('script');
                        if (script.src) {
                            newScript.src = script.src;
                        } else {
                            newScript.textContent = script.textContent;
                        }
                        document.head.appendChild(newScript);
                        setTimeout(() => document.head.removeChild(newScript), 1000);
                    });
                    
                    console.log('✅ Rainfall chart loaded successfully');
                    console.log('Chart HTML length:', rainData.chart.length);
                } else {
                    // Fallback: just insert the HTML
                    chartContainer.innerHTML = rainData.chart;
                    console.log('⚠️ Using fallback method for rainfall');
                }
                
                setTimeout(() => {
                    const plotlyDiv = chartContainer.querySelector('.plotly-graph-div');
                    if (plotlyDiv) {
                        console.log('✅ Rainfall Plotly div found:', plotlyDiv.id);
                        console.log('Rainfall div dimensions:', plotlyDiv.offsetWidth, 'x', plotlyDiv.offsetHeight);
                    } else {
                        console.error('❌ Rainfall Plotly div not found');
                    }
                }, 1000);
            } else {
                console.error('❌ Rainfall chart container not found');
            }
        } else {
            console.error('❌ Rainfall chart error:', rainData.error);
            const container = document.getElementById('rainfallChart');
            if (container) {
                container.innerHTML = 
                    `<div class="alert alert-warning">Failed to load rainfall chart: ${rainData.error || 'Unknown error'}</div>`;
            }
        }
        
        console.log('✅ All charts loaded!');
    } catch (error) {
        console.error('❌ Failed to load charts:', error);
        const errorMsg = `<div class="alert alert-danger">Error loading charts: ${error.message}</div>`;
        const tempContainer = document.getElementById('temperatureChart');
        const rainContainer = document.getElementById('rainfallChart');
        if (tempContainer) tempContainer.innerHTML = errorMsg;
        if (rainContainer) rainContainer.innerHTML = errorMsg;
    }
}

// Initialize - auto-detect location on page load
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('autoDetectBtn')?.click();
});
