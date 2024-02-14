from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    referrer = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    input_value = db.Column(db.String(255))
    html_id = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.screen_id'))
    
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

    events = db.relationship('Event', backref='user')

class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='sessions')
    ip_address = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))
    session_start_time = db.Column(db.DateTime)
    session_duration = db.Column(db.Interval)

    def __repr__(self):
        return f"<Session {self.id}>"