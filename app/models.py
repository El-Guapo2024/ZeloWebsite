from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bike(Base):
    __tablename__ = 'Bikes'
    bike_id = Column(Integer, primary_key=True)
    model_name = Column(String(50))
    purchase_date = Column(Date)
    last_maintenance = Column(Date)
    total_miles_driven = Column(Integer)
    status = Column(String(20))

    def __repr__(self):
        return(
        f"<Bike(bike_id={self.bike_id}, "
        f"model_name='{self.model_name}', "
        f"purchase_date='{self.purchase_date}',"
        f"last_maintenance='{self.last_maintenance}',"
        f"total_miles_driven='{self.total_miles_driven}',"
        f"status='{self.status}'"
        )
    
class BikeData:
    def __init__(self, bike_id, latitude, longitude, timestamp, speed, satellites):
        self.bike_id = bike_id
        self.latitude = latitude 
        self.longitude = longitude 
        self.timestamp = timestamp
        self.speed = speed
        self.satellites = satellites


