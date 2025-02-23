from flask import Flask
from flask_htmx import HTMX
from app.mqtt_subscriber import MQTTSubscriber
from app.config_reader import load_config
from flask_caching import Cache
from app.cache_manager import CacheManager
from app.db import DatabaseManager
import os 
# Import the database manager
from app.db import DatabaseManager
from app.models import Base # Import your Base model

#Applicatin Factory
def create_app():
    app = Flask(__name__)
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif os.getenv('FLASK_ENV') == 'production':
        app.config.from_object('app.config.ProductionConfig')
    else:
        print("No environment set. Defaulting to Development")
        app.config.from_object('app.config.DevelopmentConfig')
    
    # Initialize the Database Manager
    db_manager = DatabaseManager(app)
    app.db_manager = db_manager

    # Initialize the cache
    app.config['CACHE_TYPE'] = "SimpleCache" # Use "FileSystemCache" for file-based caching
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Cache timeout in seconds (optional)
    cache = Cache(app)
    cache_manager = CacheManager(cache)
    app.cache_manager = cache_manager

    # Load configuration for MQTT 
    config = load_config("app/config.yaml")
    # Initialize and start MQTT thread
    mqtt_subcriber = MQTTSubscriber(config)
    mqtt_subcriber.start()

    # Attach the MQTT thread to the app for global access
    app.mqtt_subscriber= mqtt_subcriber

    # Import routes and register them (after app is created)
    from app.routes import bike_routes
    app.register_blueprint(bike_routes)

    return app


