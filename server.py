from flask import Flask, render_template, request, jsonify, session
from weather import get_current_weather
import os
from sqlalchemy import func
from datetime import datetime, timezone
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate
import pandas as pd
import uuid
from urllib.parse import urlparse
from ip2geotools.databases.noncommercial import DbIpCity  # Using ip2geotools library for geolocation

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
    return render_template('index.html')

@app.route('/projects')
def projects():
    logger.debug('Rendering projects page')
    return render_template('projects.html')

@app.route('/policy')
def policy():
    logger.debug('Rendering policy page')
    return render_template('policy.html')

@app.route('/weather_home')
def weather_home():
    logger.debug('Rendering weather home page')
    return render_template('/weather_proj/weather_home.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    logger.info('Getting weather for city: %s', city)

    weather_data = get_current_weather(city)

    #city is not found by api
    if not weather_data['cod'] == 200:
        logger.warning('City not found: %s', city)
        return render_template('/weather_proj/city-not-found.html')

    return render_template(
        "/weather_proj/weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

@app.route('/resume')
def resume():
    logger.debug('Rendering resume page')
    return render_template('/resume.html')

@app.route('/website')
def website():
    return render_template('/website.html')



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)