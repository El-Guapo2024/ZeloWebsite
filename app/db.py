from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime 
from app.models import Bike, Base

class DatabaseManager:
    def __init__(self, database_url):
        """
        Iniitialize the Database Manager with a specific
        database URL
        """

        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def init_db(self):
        """
        Innitalize the database by creating all tables.
        """
        Base.metadata.create_all(self.engine)

    def add_bike(self, bike):
        """
        Add a new bike to the database 
        """
        try:
            self.session.add(bike)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def get_all_bikes(self):
        """
        Fetch all bikes 
        """
        return self.session.query(Bike).all()
    
    def get_all_active_bikes(self):
        """
        Fetch all actice bikes 
        """
        return self.session.query(Bike).filter_by(status='active').all()
    
    def get_bike_by_id(self, bike_id):
        """
        Fetch a bike by its ID.
        """
        return self.session.query(Bike).filter_by(bike_id=bike_id).first()
    
    def delete_bikes(self, bike_ids):
        """
        Delete bike from the database based on a list of bike IDs. 
        """

        if not bike_ids:
            return # Nohthig happens 

        try:
            self.session.query(Bike).filter(Bike.bike_id.in_(bike_ids)).delete(synchronize_session=False)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update_bike_maintenance(self, bike_id):
        """
        Update the maintenance date of a bike to today.
        """
        bike = self.get_bike_by_id(bike_id)
        if not bike:
            raise ValueError(f"Bike with ID {bike_id} does not exist.")
        
        try: 
            bike.last_maintenance = datetime.now().date()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def update_bike(self, bike_id, **kwargs):
        """
        Update the data for the bike
        """
        bike = self.get_bike_by_id(bike_id)

        if not bike: 
            raise ValueError(f"Bike with ID {bike_id} does not exists")
        try: 
            for key, value in kwargs.items():
                if hasattr(bike, key):
                    setattr(bike, key, value)
        
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def get_bikes_by_params(self, params):
        """
        Fetch bikes from the database based on dynamic parametrs

        :param params: A dictionary containing filter conditions.
            Example: {'status':'active', 'model_name': 'Mountain Bike'}

            Supports operators like {'total_miles_driven__gt': 100}
        :return: A list of Bike matching the query. 
        """

        query = self.session.query(Bike)

        for key, value in params.items():
            if '__' in key: # Handle operators like __gt ,__lt
                field, operator = key.split('__')
                column = getattr(Bike, field)
                if operator == 'gt': #Greater than 
                    query = query.filter(column > value )
                elif operator == 'lt':# Less than 
                    query = query.filter(column < value)
                elif operator == 'gte': 
                    query = query.filter(column >= value)
                elif operator == 'lte':
                    query = query.filter(column <= value)
                elif operator == 'ne':
                    query = query.filter(column != value)
                elif operator == 'like':
                    query = query.filter(column.like(f"%{value}%"))
            else:
                column = getattr(Bike, key)
                query = query.filter(column == value)

        return query.all()

    def close(self):
        """
        Close the session and engine connection.
        """
        self.session.close()
        self.engine.dispose()
        
