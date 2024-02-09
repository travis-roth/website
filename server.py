from flask import Flask, render_template, request, jsonify
from weather import get_current_weather
from models import db, Event, Screen
import os
from sqlalchemy import func
from datetime import datetime
from waitress import serve
import logging

from flask_migrate import Migrate

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

#migrate database structure changes on server start
migrate = Migrate(app, db)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the tables
with app.app_context():
    db.create_all()

@app.route('/visitor-info')
def get_visitor_info():
# Query the database to get the distinct count of user IDs
    distinct_visitors_count = Event.query.with_entities(Event.user_id).distinct().count()
    # Check if the user has visited before
    user_id = request.cookies.get('user_id')
    if user_id:
        # Get the visitor number based on the order of visits
        visitor_number = Event.query.filter(Event.user_id == user_id).distinct(Event.user_id).count()
        return jsonify({'user_order': visitor_number})
    return jsonify({'user_order': {distinct_visitors_count}})

@app.route('/log/event', methods=['POST'])
def log_event():
    # Extract event data from the request JSON
    event_data = request.json.get('eventData')
    event_type = request.json.get('eventType')
    timestamp = datetime.utcnow()  # Timestamp for the event (current time)

    # Get values from event data (assuming it's included in eventData)
    user_id = event_data.get('userId') if event_data else None
    url = event_data.get('url') if event_data else None
    referrer = event_data.get('referrer') if event_data else None
    input_value = event_data.get('inputValue') if event_data else None
    html_id = event_data.get('htmlId') if event_data else None

    #get screen data
    width = event_data.get('screenWidth') if event_data else None
    height = event_data.get('screenHeight') if event_data else None
    orientation = event_data.get('screenOrientation') if event_data else None


    # Create a new Event object and save it to the database
    new_event = Event(event_type=event_type, html_id=html_id, input_value=input_value,referrer=referrer, user_id=user_id, url=url,timestamp=timestamp)
    existing_screen = Screen.query.filter_by(width=width, height=height, orientation=orientation).first()

    if existing_screen: # Use existing screen record
        screen_id = existing_screen.screen_id
    else:               # Create new screen object
        new_screen = Screen(width=width, height=height, orientation=orientation)
        db.session.add(new_screen)
        db.session.flush()  # Flush to obtain the screen_id before committing
        screen_id = new_screen.screen_id

    new_event.screen_id = screen_id

    db.session.add(new_event)
    db.session.commit()

    # Log the event
    logger.info('Event logged successfully: %s', event_type)

    # Return a JSON response indicating success
    return jsonify({'message': 'Event logged successfully'}), 200

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

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
