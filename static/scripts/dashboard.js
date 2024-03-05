$(document).ready(function() {
    var myChart;
    var timeChart;
    var responseData; // Define a global variable to store the response data

    function updateChart(usersByCityLabels, usersByCityData, eventsByPageLabels, eventsByPageData, eventsByDayLabels, eventsByDayData, sessionsBySourceLabels, sessionsBySourceData, usersByDayLabels, usersByDayData) {
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
                    backgroundColor: '#e97911' // Set background color to orange
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Active Users',
                            color: '#fff' // Set title color to white
                        },
                        ticks: {
                            color: '#fff' // Set ticks color to white
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'City',
                            color: '#fff' // Set title color to white
                        },
                        ticks: {
                            color: '#fff' // Set ticks color to white
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff' // Set label color to white
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

        // Trigger update for the line chart with the default metric value
        updateLineChart(responseData.users_by_day_labels, responseData.users_by_day_data, 'Users');
    }

    $.ajax({
        url: '/update_data',
        method: 'GET',
        data: { startDate: '7daysAgo' },
        success: function(response) {
            responseData = response; // Store the response data in the global variable
            updateChart(response.users_by_city_labels, response.users_by_city_data, response.events_by_page_labels, response.events_by_page_data, response.events_by_day_labels, response.events_by_day_data, response.sessions_by_source_labels, response.sessions_by_source_data, response.users_by_day_labels, response.users_by_day_data);
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
                responseData = response; // Store the response data in the global variable
                updateChart(response.users_by_city_labels, response.users_by_city_data, response.events_by_page_labels, response.events_by_page_data, response.events_by_day_labels, response.events_by_day_data, response.sessions_by_source_labels, response.sessions_by_source_data, response.users_by_day_labels, response.users_by_day_data);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });

    $('#heroMetric').on('change', function() {
        var selectedMetric = $(this).val();
        if (selectedMetric === 'Users') {
            updateLineChart(responseData.users_by_day_labels, responseData.users_by_day_data, selectedMetric); // Use the global variable to access response data
        } else if (selectedMetric === 'Views') {
            updateLineChart(responseData.events_by_day_labels, responseData.events_by_day_data, selectedMetric); // Use the global variable to access response data
        }
    });

    function updateLineChart(labels, data, metricLabel) {
        if (timeChart) {
            timeChart.destroy();
        }
        var ctxLine = document.getElementById('lineChart').getContext('2d');
        timeChart = new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: metricLabel + ' per Day', // Use the selected metric label
                    data: data,
                    borderWidth: 1,
                    borderColor: '#e97911' // Set border color to orange
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: metricLabel, // Update the y-axis label based on the selected metric
                            color: '#fff' // Set title color to white
                        },
                        ticks: {
                            color: '#fff' // Set ticks color to white
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Day',
                            color: '#fff' // Set title color to white
                        },
                        ticks: {
                            color: '#fff' // Set ticks color to white
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff' // Set label color to white
                        }
                    }
                }
            }
        });
    }    
});
