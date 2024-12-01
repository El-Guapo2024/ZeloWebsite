import paho.mqtt.client as mqtt
import time
import schedule
import random
import json
from datetime import datetime

gps_topic = "Bikes/TestBike/gps_data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connect failed with code {rc}")

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

def publish_gps_data():
    try:
        gps_data = generate_gps_data()

        gps_json_data = json.dumps(gps_data)

        client.publish(gps_topic,gps_json_data)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

def generate_gps_data():
    # Generate random coordinates within reasonable bounds
    latitude = random.uniform(-11.75, -1.0)  # Tanzania's latitude range
    longitude = random.uniform(29.10, 40.49)  # Tanzania's longitude range
    altitude = random.uniform(0, 2000)  # meters
    speed = random.uniform(0, 120)  # km/h
    
    return {
        "timestamp": datetime.now().isoformat(),
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "altitude": round(altitude, 2),
        "speed": round(speed, 2),
        "satellites": random.randint(4, 12)
    }

# Create client instance
client = mqtt.Client(client_id="publisher_client_id")

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
broker_address = "mqtt.eclipseprojects.io"
port = 1883
client.connect(broker_address, port)

# Start the loop
client.loop_start()

# Setup the schedule
schedule.every(5).seconds.do(publish_gps_data)


# Wait for connection to establish
time.sleep(1)

# Publish a message
client.publish("my/topic", "Hello MQTT!")

# Keep the script running
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()