
from flask import request, jsonify
from dotenv import load_dotenv
import requests
import os
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (DateRange,Dimension,Metric,MetricType,RunReportRequest,
)

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GDA_API_KEY")

property_id = os.getenv("GA4_PROPERTY_ID")

cached_users_by_city_labels = None
cached_users_by_city_data = None
cached_events_by_page_labels = None
cached_events_by_page_data = None
cached_sessions_by_source_labels = None
cached_sessions_by_source_data = None
cached_users_by_day_labels = None
cached_users_by_day_data = None
cached_users_by_time_labels = None
cached_users_by_time_data = None


def fetch_data(start_date, end_date="today"):
    global cached_users_by_city_labels, cached_users_by_city_data, cached_events_by_page_labels, cached_events_by_page_data, cached_sessions_by_source_labels, cached_sessions_by_source_data, cached_users_by_day_labels, cached_users_by_day_data, cached_users_by_hour_labels, cached_users_by_hour_data

    # Fetch data from Google Analytics API
    users_by_city = run_custom_report(
        metrics=["activeUsers"],
        dimensions=["city"],
        start_date=start_date,
        end_date=end_date
    )

    events_by_page = run_custom_report(
        metrics=["screenPageViews"],
        dimensions=["pageTitle"],
        start_date=start_date,
        end_date=end_date
    )

    sessions_by_source = run_custom_report(
        metrics=["sessions"],
        dimensions=["sessionSource"],
        start_date=start_date,
        end_date=end_date
    )

    users_by_day = run_custom_report(
        metrics=["activeUsers"],
        dimensions=["date"],
        start_date=start_date,
        end_date=end_date
    )    

    users_by_hour = run_custom_report(
        metrics=["activeUsers"],
        dimensions=["hour"],
        start_date=start_date,
        end_date=end_date
    )  

    # Preprocess and return the data
    users_by_city_labels, users_by_city_data = preprocess_response(users_by_city)
    events_by_page_labels, events_by_page_data = preprocess_response(events_by_page)
    sessions_by_source_labels, sessions_by_source_data = preprocess_response(sessions_by_source)
    users_by_day_labels, users_by_day_data = preprocess_response(users_by_day)
    users_by_hour_labels, users_by_hour_data = preprocess_response(users_by_hour)

    # Fill in missing dates with 0 users and order arrays by date
    filled_dates, filled_data = fill_and_order_dates(users_by_day_labels, users_by_day_data, start_date, end_date)

    return {
        'users_by_city_labels': users_by_city_labels,
        'users_by_city_data': users_by_city_data,
        'events_by_page_labels': events_by_page_labels,
        'events_by_page_data': events_by_page_data,
        'sessions_by_source_labels': sessions_by_source_labels,
        'sessions_by_source_data': sessions_by_source_data,
        'users_by_day_labels': filled_dates,
        'users_by_day_data': filled_data,
        'users_by_hour_labels': users_by_hour_labels,
        'users_by_hour_data': users_by_hour_data
    }

def fill_and_order_dates(labels, data, start_date, end_date):
    """
    Fill in missing dates between start_date and end_date with 0 values and order arrays by date.
    
    Args:
        labels (list): List of dates in YYYYMMDD format.
        data (list): Corresponding data points.
        start_date (str): Start date in YYYYMMDD format.
        end_date (str): End date in YYYYMMDD format.
    
    Returns:
        Tuple containing filled and ordered dates and corresponding filled and ordered data points.
    """
    filled_dates = []
    filled_data = []

    start_date_as_datetime = parse_date_term(start_date)
    end_date_as_datetime = parse_date_term(end_date)
    
    current_date = datetime.strptime(start_date_as_datetime, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_as_datetime, "%Y-%m-%d")
    
    # Fill in missing dates with 0 values
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        filled_dates.append(date_str)
        
        if date_str in labels:
            index = labels.index(date_str)
            filled_data.append(data[index])
        else:
            filled_data.append(0)
        
        current_date += timedelta(days=1)
    
    return filled_dates, filled_data

def parse_date_term(date_term):
    """
    Parses date terms like "yesterday", "today", "30daysAgo" into datetime format.

    Args:
        date_term (str): Date term string.

    Returns:
        str: Date string in "%Y-%m-%d" format.
    """
    if date_term == "yesterday":
        return (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_term == "today":
        return datetime.today().strftime("%Y-%m-%d")
    elif date_term.endswith("daysAgo"):
        days_ago = int(date_term[:-7])
        return (datetime.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    else:
        # Default to today's date
        return datetime.today().strftime("%Y-%m-%d")

def get_data():
    global cached_users_by_city_labels, cached_users_by_city_data, cached_events_by_page_labels, cached_events_by_page_data, cached_sessions_by_source_labels, cached_sessions_by_source_data, cached_users_by_day_labels, cached_users_by_day_data, cached_users_by_hour_labels, cached_users_by_hour_data

    start_date = request.args.get('startDate')

    if start_date is None:
        # Set a default start date, e.g., 7 days ago from today
        default_start_date = "7daysAgo"
        start_date = default_start_date

    if cached_users_by_city_labels is None or cached_users_by_city_data is None \
            or cached_events_by_page_labels is None or cached_events_by_page_data is None \
            or cached_sessions_by_source_labels is None or cached_sessions_by_source_data is None \
            or cached_users_by_day_labels is None or cached_users_by_day_data is None \
            or cached_users_by_hour_labels is None or cached_users_by_hour_data is None:
        # Fetch data only if it hasn't been fetched before
        data = fetch_data(start_date)
        cached_users_by_city_labels = data['users_by_city_labels']
        cached_users_by_city_data = data['users_by_city_data']
        cached_events_by_page_labels = data['events_by_page_labels']
        cached_events_by_page_data = data['events_by_page_data']
        cached_sessions_by_source_labels = data['sessions_by_source_labels']
        cached_sessions_by_source_data = data['sessions_by_source_data']
        cached_users_by_day_labels = data['users_by_day_labels']
        cached_users_by_day_data = data['users_by_day_data']
        cached_users_by_hour_labels = data['users_by_hour_labels']
        cached_users_by_hour_data = data['users_by_hour_data']

    return {
        'users_by_city_labels': cached_users_by_city_labels,
        'users_by_city_data': cached_users_by_city_data,
        'events_by_page_labels': cached_events_by_page_labels,
        'events_by_page_data': cached_events_by_page_data,
        'sessions_by_source_labels': cached_sessions_by_source_labels,
        'sessions_by_source_data': cached_sessions_by_source_data,
        'users_by_day_labels': cached_users_by_day_labels,
        'users_by_day_data': cached_users_by_day_data,
        'users_by_hour_labels': cached_users_by_hour_labels,
        'users_by_hour_data': cached_users_by_hour_data
    }

def update_data():
    start_date = request.args.get('startDate')

    # Fetch updated data based on the new start date
    data = fetch_data(start_date)

    return jsonify(data)


def print_run_report_response(response):
    """Prints results of a runReport call."""
    print(f"{response.row_count} rows received")
    for dimensionHeader in response.dimension_headers:
        print(f"Dimension header name: {dimensionHeader.name}")
    for metricHeader in response.metric_headers:
        metric_type = MetricType(metricHeader.type_).name
        print(f"Metric header name: {metricHeader.name} ({metric_type})")

    print("Report result:")
    for rowIdx, row in enumerate(response.rows):
        print(f"\nRow {rowIdx}")
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].name
            print(f"{dimension_name}: {dimension_value.value}")

        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            print(f"{metric_name}: {metric_value.value}")

def run_custom_report(metrics=['activeUsers'], dimensions=['city'], start_date="7daysAgo", end_date="today", property_id=property_id):
    """
    Runs a custom report with multiple metrics and dimensions.
    
    Args:
        metrics (list): List of metric names.
        dimensions (list): List of dimension names.
        start_date (str): Start date for the report in YYYY-MM-DD format. Default is "7daysAgo".
        end_date (str): End date for the report in YYYY-MM-DD format. Default is "today".
        property_id (str): Google Analytics 4 property ID. Default is property_id global variable.
    """
    client = BetaAnalyticsDataClient()

    # Prepare metrics
    report_metrics = [Metric(name=metric) for metric in metrics]
    
    # Prepare dimensions
    report_dimensions = [Dimension(name=dimension) for dimension in dimensions]

    # Create report request
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=report_dimensions,
        metrics=report_metrics,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    
    # Execute report request
    response = client.run_report(request)
    return response

def preprocess_response(response):
    """
    Preprocesses the response from Google Analytics Data API into a format suitable for charting.

    Args:
        response: Response object from Google Analytics Data API.

    Returns:
        Tuple containing labels and data points for the chart.
    """
    labels = []
    data = []

    # Iterate through rows in the response
    for row in response.rows:
        # Assuming the first dimension is the label for the chart
        label = row.dimension_values[0].value
        labels.append(label)

        # Assuming the first metric represents the data point for the chart
        data_point = int(row.metric_values[0].value)
        data.append(data_point)

    return labels, data