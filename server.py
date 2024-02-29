from flask import Flask, render_template, request, jsonify
from weather import get_current_weather
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler
from google_data import run_custom_report, preprocess_response, get_data, update_data

app = Flask(__name__)

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

@app.route('/dashboard')
def dashboard():
    data = get_data()
    app.logger.debug("Dashboard data: %s", data)
    return render_template("dashboard.html", 
                           users_by_city_labels=data['users_by_city_labels'],
                           users_by_city_data=data['users_by_city_data'],
                           events_by_page_labels=data['events_by_page_labels'],
                           events_by_page_data=data['events_by_page_data'],
                           sessions_by_source_labels=data['sessions_by_source_labels'],
                           sessions_by_source_data=data['sessions_by_source_data'],
                           users_by_day_labels=data['users_by_day_labels'],
                           users_by_day_data=data['users_by_day_data'],
                           users_by_hour_labels=data['users_by_hour_labels'],
                           users_by_hour_data=data['users_by_hour_data'])

@app.route('/update_data')
def update():
    response_data = update_data()
    app.logger.debug("Update data response: %s", response_data)
    return response_data




if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)