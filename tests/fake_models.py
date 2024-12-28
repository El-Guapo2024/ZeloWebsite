import random 
import json 
from datetime import datetime
import paho.mqtt.client as mqtt
import schedule

class FakeBike:
    def __init__(self, bike_id, mqtt_client):
        self.bike_id = bike_id
        self.gps_topic = f'Bikes/{self.bike_id}/gps_data'
        self.mqtt_client = mqtt_client

    def generate_gps_data(self):
        """Generate random GPS data."""
        latitude = random.uniform(-11.75, -1.0)
        longitude = random.uniform(29.10, 40.49)
        altitude = random.uniform(0,2000)
        speed = random.uniform(0,120)

        return {
            'bike_id': self.bike_id,
            'timestamp': datetime.now().isoformat(),
            'latitude': round(latitude, 6),
            'longitude': round(longitude),
            'altitude': round(altitude),
            'speed': round(speed, 2),
            'satellites': random.randint(4,12)
        }
    
    def publish_gps_data(self):
        """Publish generated GPS data to the MQTT topic."""
        gps_data = self.generate_gps_data()
        gps_json_data = json.dumps(gps_data)

        self.mqtt_client.publish(self.gps_topic, gps_json_data)

        print(f"published to {self.gps_topic}: {gps_json_data}")

    def schedule_updates(self):
        """Schedule this bike's updates to the MQTT topic."""
        interval = random.randint(25, 35)
        print(f"Scheduling updates for {self.bike_id} every {interval} seconds")

        schedule.every(interval).seconds.do(self.publish_gps_data)

