import paho.mqtt.client as mqtt
import time
import schedule
from fake_models import FakeBike 
# import random
# import json
# from datetime import datetime
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected succesfully")
    else:
        print(f"Connect failed with code {rc}")

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Create client instance 
client = mqtt.Client(client_id="publisher_client_id")

# Set Callbacks 
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
broker_address = "mqtt.eclipseprojects.io"
port = 1883
client.connect(broker_address, port)

# Start the loop 
client.loop_start()

# Create Bike instance and schedule their data publishing
bikes = [FakeBike(f"Bike{i}", client) for i in range(0,10)]
for bike in bikes:
    bike.schedule_updates()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
finally:
    client.loop_stop()
    client.disconnect()
