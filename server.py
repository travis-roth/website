from flask import Flask, render_template, request, jsonify
from weather import get_current_weather
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler
from google_data import get_data
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta


app = Flask(__name__)
scheduler = APScheduler()

DEFAULT_START_DATE = "yesterday"

cached_data = {
    "yesterday": None,
    "7daysAgo": None,
    "30daysAgo": None
}

last_cache_time = None
cache_duration = timedelta(days=1)  # Cache duration is set to 1 day

# logging
def configure_logging(app):
    logging.basicConfig(level=logging.DEBUG)
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

logger = logging.getLogger(__name__)

configure_logging(app)

@app.route('/')
@app.route('/index')
def index():

    logger.debug('Rendering index page')
    return render_template('index.html', current_page='home')

@app.route('/projects')
def projects():
    logger.debug('Rendering projects page')
    return render_template('projects.html', current_page='projects')

@app.route('/policy')
def policy():
    logger.debug('Rendering policy page')
    return render_template('policy.html', current_page='policy')

@app.route('/weather_home')
def weather_home():
    logger.debug('Rendering weather home page')
    return render_template('/weather_proj/weather_home.html', current_page='projects')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    logger.info('Getting weather for city: %s', city)

    weather_data = get_current_weather(city)

    #city is not found by api
    if not weather_data['cod'] == 200:
        logger.warning('City not found: %s', city)
        return render_template('/weather_proj/city-not-found.html', current_page='projects')

    return render_template(
        "/weather_proj/weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}", 
        current_page='projects'
    )



@app.route('/dubgrub')
def dubgrub():
    logger.debug('Rendering dubgrub page')
    return render_template('/dubgrub.html', current_page='dubgrub')

@app.route('/bloodworks')
def bloodworks():
    logger.debug('Rendering bloodworks page')
    return render_template('/bloodworks.html', current_page='bloodworks')

@app.route('/edfr')
def edfr():
    logger.debug('Rendering edfr page')
    return render_template('/edfr.html', current_page='edfr')

@app.route('/website')
def website():
    return render_template('/website.html')

def fetch_and_cache_data():
    global cached_data
    # Fetch data from the Google Analytics API
    # This is where you'd call your fetch_data function
    # For demonstration, I'll assume fetch_data returns some dummy data
    cached_data['yesterday'] = get_data("yesterday")
    cached_data['7daysAgo'] = get_data("7daysAgo")
    cached_data['30daysAgo'] = get_data("30daysAgo")

    last_cache_time = datetime.now()

    app.logger.debug("Cached Data yesterday: %s", cached_data['yesterday'])
    app.logger.debug("Cached Data 7daysAgo: %s", cached_data['7daysAgo'])
    app.logger.debug("Cached Data 30daysAgo: %s", cached_data['30daysAgo'])



# manually trigger caching
@app.route('/cache_data')
def cache_data():
    fetch_and_cache_data()
    return 'Data cached successfully'

@app.route('/dashboard')
def dashboard():
    global cached_data_30daysAgo,cached_data_7daysAgo,cached_data_yesterday
    start_date = request.args.get('startDate',DEFAULT_START_DATE)
    app.logger.debug("Dashboard data: %s", start_date, cached_data[start_date])
    return render_template("dashboard.html",
                           users_by_city_labels=cached_data[start_date]['users_by_city_labels'],
                           users_by_city_data=cached_data[start_date]['users_by_city_data'],
                           events_by_page_labels=cached_data[start_date]['events_by_page_labels'],
                           events_by_page_data=cached_data[start_date]['events_by_page_data'],
                           sessions_by_source_labels=cached_data[start_date]['sessions_by_source_labels'],
                           sessions_by_source_data=cached_data[start_date]['sessions_by_source_data'],
                           users_by_day_labels=cached_data[start_date]['users_by_day_labels'],
                           users_by_day_data=cached_data[start_date]['users_by_day_data'],
                           users_by_hour_labels=cached_data[start_date]['users_by_hour_labels'],
                           users_by_hour_data=cached_data[start_date]['users_by_hour_data'])

@app.route('/update_data')
def update():
    start_date = request.args.get('startDate')
    response_data = {
        "users_by_city_labels": cached_data[start_date]['users_by_city_labels'],
        "users_by_city_data": cached_data[start_date]['users_by_city_data'],
        "events_by_page_labels": cached_data[start_date]['events_by_page_labels'],
        "events_by_page_data": cached_data[start_date]['events_by_page_data'],
        "sessions_by_source_labels": cached_data[start_date]['sessions_by_source_labels'],
        "sessions_by_source_data": cached_data[start_date]['sessions_by_source_data'],
        "users_by_day_labels": cached_data[start_date]['users_by_day_labels'],
        "users_by_day_data": cached_data[start_date]['users_by_day_data'],
        "users_by_hour_labels": cached_data[start_date]['users_by_hour_labels'],
        "users_by_hour_data": cached_data[start_date]['users_by_hour_data']
    }
    return response_data

@scheduler.task('interval', id='cache_job', days=1)
def scheduled_cache_job():
    fetch_and_cache_data()

if __name__ == "__main__":
    fetch_and_cache_data()
    scheduler.init_app(app)
    scheduler.start()
    serve(app, host="0.0.0.0", port=8000)