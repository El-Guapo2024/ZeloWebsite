from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
# Define Bike Model 

Base = declarative_base()

class Bike(Base):
    __tablename__ = 'Bikes'

    bike_id = Column(Integer, primary_key=True)
    model_name = Column(String(50))
    purchase_date = Column(Date)
    last_maintenance = Column(Date)
    total_miles_driven = Column(Float)
    status = Column(String(20))

    def __repr__(self):
        return(
        f"<Bike(bike_id={self.bike_id}, "
        f"model_name='{self.model_name}', "
        f"purchase_data='{self.purchase_date}',"
        f"last_maintenance='{self.last_maintenance}',"
        f"total_miles_driven='{self.total_miles_driven}',"
        f"status='{self.status}'"
        )
    

