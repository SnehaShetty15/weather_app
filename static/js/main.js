// Main JavaScript for Smart Weather App

// Utility functions
const Utils = {
    // Format date
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'short', 
            month: 'short', 
            day: 'numeric' 
        });
    },

    // Get weather icon URL
    getWeatherIcon: (iconCode) => {
        return `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
    },

    // Show error message
    showError: (message) => {
        alert(`Error: ${message}`);
    },

    // Show loading
    showLoading: () => {
        document.getElementById('loadingSpinner')?.style.setProperty('display', 'block');
        document.getElementById('weatherDashboard')?.style.setProperty('display', 'none');
    },

    // Hide loading
    hideLoading: () => {
        document.getElementById('loadingSpinner')?.style.setProperty('display', 'none');
        document.getElementById('weatherDashboard')?.style.setProperty('display', 'block');
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
