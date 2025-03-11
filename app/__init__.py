from flask import Flask
from flask_htmx import HTMX
from app.mqtt_subscriber import MQTTSubscriber
from app.config_reader import load_config
from flask_caching import Cache
from app.cache_manager import CacheManager
from app.db import DatabaseManager
import os 
from dotenv import load_dotenv

# Import the database manager
from app.db import DatabaseManager
from app.models import Base # Import your Base model

# Application Factory
def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)
    
    # Force production config when FLASK_ENV is set to production
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object('app.config.ProductionConfig')
        print("Using Production Configuration")
    else:
        app.config.from_object('app.config.DevelopmentConfig')
        print("Using Development Configuration")
    
    try:
        # Initialize the Database Manager
        db_manager = DatabaseManager(app)
        app.db_manager = db_manager
        print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

    # Initialize the cache
    app.config['CACHE_TYPE'] = "SimpleCache"
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    cache = Cache(app)
    cache_manager = CacheManager(cache)
    app.cache_manager = cache_manager

    try:
        # Load configuration for MQTT 
        config = load_config("app/config.yaml")
        # Initialize and start MQTT thread
        mqtt_subcriber = MQTTSubscriber(config)
        mqtt_subcriber.start()
        # Attach the MQTT thread to the app for global access
        app.mqtt_subscriber = mqtt_subcriber
    except Exception as e:
        print(f"Error initializing MQTT: {str(e)}")
        # Don't raise here as MQTT is not critical for the app to run

    # Import routes and register them (after app is created)
    from app.routes import bike_routes
    app.register_blueprint(bike_routes)

    return app


