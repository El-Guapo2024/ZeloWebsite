import paho.mqtt.client as mqtt
import time

gps_topic = "Bikes/TestBike/gps_data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("Bikes/TestBike/gps_data")  # Subscribe to the topic
    else:
        print(f"Connect failed with code {rc}")

def on_message(client, userdata, message):
    gps_data = message.payload.decode()
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Create client instance
client = mqtt.Client(client_id="subscriber_client_id")

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
broker_address = "mqtt.eclipseprojects.io"
port = 1883
client.connect(broker_address, port)

# Start the loop
client.loop_start()

# Wait for connection to establish
time.sleep(1)

# Subscribe to a topic
client.subscribe("my/topic")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()