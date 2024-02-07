from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
