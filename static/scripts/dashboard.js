$(document).ready(function() {
    var myChart;
    var timeChart;

    function updateChart(usersByCityLabels, usersByCityData, eventsByPageLabels, eventsByPageData, sessionsBySourceLabels, sessionsBySourceData, usersByDayLabels, usersByDayData) {
        if (myChart) {
            myChart.destroy();
        }
        if (timeChart) {
            timeChart.destroy();
        }
    
        var ctx = document.getElementById('myChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: usersByCityLabels,
                datasets: [{
                    label: 'Active Users by City',
                    data: usersByCityData,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Active Users'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'City'
                        }
                    }
                }
            }
        });
    
        // Render table for events by page
        var tableHTML = '<table><thead><tr><th>Page</th><th>Views</th></tr></thead><tbody>';
        for (var i = 0; i < eventsByPageLabels.length; i++) {
            tableHTML += '<tr><td>' + eventsByPageLabels[i] + '</td><td>' + eventsByPageData[i] + '</td></tr>';
        }
        tableHTML += '</tbody></table>';
        $('#eventsByPageTable').html(tableHTML);
    
        // Render table for sessions by source
        var sessionsTableHTML = '<table><thead><tr><th>Source</th><th>Sessions</th></tr></thead><tbody>';
        for (var i = 0; i < sessionsBySourceLabels.length; i++) {
            sessionsTableHTML += '<tr><td>' + sessionsBySourceLabels[i] + '</td><td>' + sessionsBySourceData[i] + '</td></tr>';
        }
        sessionsTableHTML += '</tbody></table>';
        $('#sessionsBySourceTable').html(sessionsTableHTML);
    
        // Render line chart for users per day
        var ctxLine = document.getElementById('lineChart').getContext('2d');
        timeChart = new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: usersByDayLabels,
                datasets: [{
                    label: 'Users per Day',
                    data: usersByDayData,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Users'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Day'
                        }
                    }
                }
            }
        });

    }
    $.ajax({
        url: '/update_data',
        method: 'GET',
        data: { startDate: '7daysAgo' },
        success: function(response) {
            updateChart(response.users_by_city_labels, response.users_by_city_data, response.events_by_page_labels, response.events_by_page_data, response.sessions_by_source_labels, response.sessions_by_source_data, response.users_by_day_labels, response.users_by_day_data);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });

    $('#startDate').on('change', function() {
        var startDate = $(this).val();
        $.ajax({
            url: '/update_data',
            method: 'GET',
            data: { startDate: startDate },
            success: function(response) {
                updateChart(response.users_by_city_labels, response.users_by_city_data, response.events_by_page_labels, response.events_by_page_data, response.sessions_by_source_labels, response.sessions_by_source_data, response.users_by_day_labels, response.users_by_day_data);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});
