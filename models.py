from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    referrer = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.String(255), nullable=True)
    input_value = db.Column(db.String(255), nullable=True)
    html_id = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
