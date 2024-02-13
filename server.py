from flask import Flask, render_template, request, jsonify, session
from weather import get_current_weather
from models import db, Event, Screen, User, UserSession
import os
from sqlalchemy import func
from datetime import datetime, timezone
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler

from flask_migrate import Migrate

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

#migrate database structure changes on server start
migrate = Migrate(app, db)

# logging
def configure_logging(app):
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
logger = logging.getLogger(__name__)

configure_logging(app)

app.secret_key = os.getenv("SECRET_KEY")

# Create the tables
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/visitor-info')
def get_visitor_info():
# Query the database to get the distinct count of user IDs
    distinct_visitors_count = User.query.with_entities(User.cookie_id).distinct().count()
    # Check if the user has visited before
    user_cookie = request.cookies.get('cookie_id')
    if user_cookie:
        # Get the visitor number based on the order of visits
        visitor_number = User.query.filter(User.cookie_id == user_cookie).distinct(User.cookie_id).count()
        return jsonify({'user_order': visitor_number})
    return jsonify({'user_order': {distinct_visitors_count}})

@app.route('/log/event', methods=['POST'])
def log_event():
    # Extract event data from the request JSON
    event_data = request.json.get('eventData')
    event_type = request.json.get('eventType')
    timestamp = datetime.now(timezone.utc)  # Timestamp for the event (current time)

    # Get values from event data (assuming it's included in eventData)
    cookie_id = event_data.get('cookieId') if event_data else None
    url = event_data.get('url') if event_data else None
    referrer = event_data.get('referrer') if event_data else None
    input_value = event_data.get('inputValue') if event_data else None
    html_id = event_data.get('htmlId') if event_data else None

    #get screen data
    width = event_data.get('screenWidth') if event_data else None
    height = event_data.get('screenHeight') if event_data else None
    orientation = event_data.get('screenOrientation') if event_data else None

    # Get or create a user based on the cookie
    cookie_id = request.cookies.get('cookie_id')
    if cookie_id:
        # Check if the cookie is associated with any user
        user = User.query.filter_by(cookie_id=cookie_id).first()
        if user:
            user = user.user_id
        else:
            # Create a new user and associate the cookie with it
            new_user = User(cookie_id=cookie_id)
            db.session.add(new_user)
            db.session.commit()
            user=new_user.user_id
    else:
        # Create a new user without a cookie ID
        user = User()
        db.session.add(user)
        db.session.commit()
        user_id = user.user_id

    user_id = user.user_id

    #get session data
    languages = event_data.get('languages') if event_data else None
    user_agent = event_data.get('userAgent') if event_data else None
    if 'session_start_time' not in session:
        session['session_start_time'] = datetime.now(timezone.utc)
    session_duration = timestamp - session['session_start_time']

    # Create a new Event object and save it to the database
    new_event = Event(event_type=event_type, html_id=html_id, input_value=input_value,referrer=referrer, user_id=user_id, url=url,timestamp=timestamp)
    new_user_session = UserSession(remote_addr=request.remote_addr, user_id=user_id,languages=languages, user_agent=user_agent, session_start_time=session['session_start_time'], session_duration=session_duration)
    
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
    db.session.add(new_user_session)
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