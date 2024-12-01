import random
from datetime import datetime

def generate_fake_data(bikes=None):
    bike_data = {}
    if not bikes:
        return bike_data

    for bike in bikes:
        bike_dict = bike.to_dict()
        bike_dict.update({
            "latitude": round(random.uniform(40.0, 41.0), 6),
            "longitude": round(random.uniform(-74.0, -73.0), 6),
            "speed": round(random.uniform(0, 30), 1),
            "battery": random.randint(20, 100),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        bike_data[f"bike_{bike.id}"] = bike_dict
    
    return bike_data

def generate_fake_location_data(bikes):
    bike_data = {}
    for bike in bikes:
        bike_data[f"bike_{bike['bike_id']}"] = {
            "bike_id": bike['bike_id'],
            "model_name": bike['model_name'],
            "latitude": round(random.uniform(40.0, 41.0), 6),
            "longitude": round(random.uniform(-74.0, -73.0), 6),
            "speed": round(random.uniform(0, 30), 1),
            "total_miles_driven": bike['total_miles_driven'],
            "last_maintenance": bike['last_maintenance'],
            "status": bike['status'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return bike_data