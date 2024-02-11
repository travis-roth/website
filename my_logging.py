import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
