from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    referrer = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
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