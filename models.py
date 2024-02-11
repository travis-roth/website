from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    referrer = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    input_value = db.Column(db.String(255))
    html_id = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)
     # Foreign key column referencing screen_info
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.screen_id'))
    screen_info = db.relationship('Screen', backref='events')
    
class Screen(db.Model):
    __tablename__ = 'screens'

    screen_id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    orientation = db.Column(db.String(20))

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    cookie_id = db.Column(db.String(255), unique=True)
    # Add other user-related fields as needed

class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='sessions')
    remote_addr = db.Column(db.String(255))
    language = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))
    # Add other session-related fields as needed