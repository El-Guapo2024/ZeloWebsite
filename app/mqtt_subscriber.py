import paho.mqtt.client as mqtt
import json 
from app.models import BikeData
from threading import Thread, Event

class MQTTSubscriber(Thread):
    def __init__(self, config):
        """
        Initialize the MQTT with config and shared_dictionary
        : param config: Configuration dictionary loaded from YAML
        """
        super().__init__()
        self.broker_address = config["MQTT"]["broker_address"]
        self.port = config["MQTT"]["port"]
        self.client_id = config["MQTT"]["client_id"]
        self.bike_ids = config["MQTT"]["bike_ids"]

        # Initialize the shared dictionary as a member of this class
        self.shared_bike_data = {}
        # Thread control 
        self.stop_event = Event()


    def setup_client(self):
        """Initialize the MQTT client"""
        self.client = mqtt.Client(client_id=self.client_id, clean_session=False)

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            for bike_id in self.bike_ids:
                self.subscribe_to_bike(bike_id) 
        else: 
            print(f"Connect failed with code {rc}")

    def on_message(self, client, userdata, message):
        """Callback for when a message is received."""
        try:
            gps_data = json.loads(message.payload.decode())
            bike_id = gps_data['bike_id']
            latitude = gps_data['latitude']
            longitude = gps_data['longitude']
            speed = gps_data['speed']
            timestamp = gps_data['timestamp']
            satellites = gps_data['satellites']

            # Update shared dictionary 
            self.shared_bike_data[bike_id] = BikeData(bike_id, latitude,
                longitude, timestamp, speed, satellites)
            #print(f"Updated {bike_id}: {latitude}, {longitude} at {timestamp}")
        
        except (json.JSONDecodeError, KeyError) as e :
            print(f"Failed to process message: {e}")

    def connect(self):
        """Connect to the MQTT Broker"""
        self.setup_client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port)

    def subscribe_to_bike(self, bike_id):
        """Subscribe to a specific bike's GPS topic"""
        topic = f"Bikes/Bike{bike_id}/gps_data"
        self.client.subscribe(topic)
        #print(f"Subscribe to {topic}")

    def start_loop(self):
        """Start the MQTT client loop."""
        self.client.loop_start()

    def stop_loop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()

    def disconect(self):
        """Disconnect from the MQTT broker."""
        self.client.disconnect()

    def get_shared_data(self)->dict:
        """
        Getter method to access the shared bike dictionary.

        :return: The shared bike data dictionary 
        """
        return self.shared_bike_data
    
    def run(self):
        """Run method executed when the thread starts."""
        print("Starting MQTT Thread...")

        # Connect to the broker
        try: 
            self.connect()
            self.start_loop()
            while not self.stop_event.is_set():
                self.stop_event.wait(1)
        except Exception as e:
            print(f"Error in MQTT Thread: {e}")
        except KeyboardInterrupt:
            print("Stopping MQTT Thread...")
            self.stop_loop()
            self.disconect()

    def stop(self):
        """Signal the thread to stop."""
        print("Stopping MQTT Thread...")
        self.stop_event.set()