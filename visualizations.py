from models import Event, Screen, User, UserSession
import plotly.graph_objects as go
import pandas as pd

from flask import jsonify
from models import Event
from server import db

# Function to retrieve Sankey diagram data
def get_sankey_data():
    # Query event data to get transitions between URLs
    transitions = db.session.query(Event.referrer, Event.url, db.func.count().label('count')) \
                    .filter(Event.referrer != '', Event.url != '') \
                    .group_by(Event.referrer, Event.url) \
                    .all()

    # Prepare nodes and links for the Sankey diagram
    nodes = set()
    links = []
    for referrer, url, count in transitions:
        nodes.add(referrer)
        nodes.add(url)
        links.append({'source': referrer, 'target': url, 'value': count})

    # Convert nodes set to a sorted list
    nodes = sorted(list(nodes))

    return {'nodes': nodes, 'links': links}