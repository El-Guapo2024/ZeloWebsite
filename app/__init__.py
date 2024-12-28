from flask import Flask
from flask_htmx import HTMX
from app.mqtt_subscriber import MQTTSubscriber
from app.config_reader import load_config
from flask_caching import Cache
from app.cache_manager import CacheManager
# import pypugjs.ext.jinja 
# from flask_htmx import HTMX s

#Applicatin Factory
def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = "SimpleCache" # Use "FileSystemCache" for file-based caching
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Cache timeout in seconds (optional)
    cache = Cache(app)
    cache_manager = CacheManager(cache)
    app.cache_manager = cache_manager
    # app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")
    # Should we add pug in the future for now i want to learn html better
    config = load_config("app/config.yaml")
    # Initialize HTMX
    htmx = HTMX(app)

    # Initialize and start MQTT thread
    mqtt_subcriber = MQTTSubscriber(config)
    mqtt_subcriber.start()

    # Attach the MQTT thread to the app for global access
    app.mqtt_subscriber= mqtt_subcriber

    # Import routes and register them (after app is created)
    from app.routes import bike_routes
    app.register_blueprint(bike_routes)

    return app 


