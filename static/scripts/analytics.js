// static/js/analytics.js

// Initialize Leaflet map
var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Page views data passed from Flask backend
var pageViewsData = {{ page_views | safe }};
var pageTitles = pageViewsData.map(function(entry) { return entry.page_title; });
var pageViews = pageViewsData.map(function(entry) { return entry.page_views; });

// Daily users data passed from Flask backend
var dailyUsersData = {{ daily_users | safe }};
var dates = dailyUsersData.map(function(entry) { return entry.date; });
var dailyUsers = dailyUsersData.map(function(entry) { return entry.users; });

document.addEventListener('DOMContentLoaded', function() {
    // User locations data passed from Flask backend
    var userLocations = {{ user_locations | safe }};

    // Add markers for each user location
    userLocations.forEach(function(location) {
        L.marker([location.lat, location.lng]).addTo(map);
    });

    // Initialize Page Views chart
    var pageViewsChart = new Chart(document.getElementById('pageViewsChart'), {
        type: 'bar',
        data: {
            labels: pageTitles,
            datasets: [{
                label: 'Page Views',
                data: pageViews,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Initialize Daily Users chart
    var dailyUsersChart = new Chart(document.getElementById('dailyUsersChart'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Daily Users',
                data: dailyUsers,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
