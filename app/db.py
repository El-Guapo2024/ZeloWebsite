from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime 
from app.models import Bike
import logging 
from contextlib import contextmanager


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import logging
from contextlib import contextmanager
import os  # Import the 'os' module
from app.models import Base

class DatabaseManager:
    def __init__(self, app=None):
        """
        Initialize the Database Manager with optional Flask application instance.
        """
        self.engine = None
        self.Session = None
        self.logger = logging.getLogger(__name__)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the Database Manager with a Flask application instance.
        """
        database_url = app.config['SQLALCHEMY_DATABASE_URI']  # Get database URL from config
        self.init_db(database_url)  # Initialize db when the app starts

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if self.Session:
                self.Session.remove()

    def init_db(self, database_url):
        """
        Initialize the direct database connection - use this for scripts/tasks
        """
        self.engine = create_engine(database_url, echo=False, pool_pre_ping=True)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        # Now create all tables
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """
        Context manager for a transactional session.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error in session: {e}")
            raise e
        finally:
            session.close()

    def dispose(self):
        """
        Dispose of the engine connection.
        """
        if self.engine:
            self.engine.dispose()

    def add_bike(self, bike):
        """
        Add a new bike to the database
        """
        with self.session_scope() as session:
            session.add(bike)

        print("added bike to db")

    def get_all_bikes(self):
        """
        Fetch all bikes
        """
        with self.session_scope() as session:
            bikes = session.query(Bike).all()
            session.expunge_all()
            return bikes

    def get_all_active_bikes(self):
        """
        Fetch all actice bikes 
        """
        with self.session_scope() as session:
            return session.query(Bike).filter_by(status='active').all()
    
    def get_bike_by_id(self, bike_id):
        """
        Fetch a bike by its ID.
        """
        with self.session_scope() as session:
            bike = session.query(Bike).filter_by(bike_id=bike_id).first()
            session.expunge_all()
            return bike
    
    def delete_bikes(self, bike_ids):
        """
        Delete bike from the database based on a list of bike IDs. 
        """
        if not bike_ids:
            return # Nothing happens 
        with self.session_scope() as session:
            session.query(Bike).filter(Bike.bike_id.in_(bike_ids)).delete(synchronize_session=False)

    def update_bike_maintenance(self, bike_id):
        """
        Update the maintenance date of a bike to today.
        """
        with self.session_scope() as session:
            bike = session.query(Bike).filter_by(bike_id=bike_id).first()
            if not bike:
                raise ValueError(f"Bike with ID {bike_id} does not exist.")
            bike.last_maintenance = datetime.now().date()
 
    def update_bike(self, bike_id, **kwargs):
        """
        Update the data for the bike
        """
        with self.session_scope() as session:
            bike = session.query(Bike).filter_by(bike_id=bike_id).first()
            if not bike:
                raise ValueError(f"Bike with ID {bike_id} does not exist.")
            for key, value in kwargs.items():
                if hasattr(bike, key):
                    setattr(bike, key, value)

    def get_bikes_by_params(self, params):
        """
        Fetch bikes from the database based on dynamic parametrs

        :param params: A dictionary containing filter conditions.
            Example: {'status':'active', 'model_name': 'Mountain Bike'}

            Supports operators like {'total_miles_driven__gt': 100}
        :return: A list of Bike matching the query. 
        """
        with self.session_scope() as session:
            query = session.query(Bike)
            for key, value in params.items():
                if '__' in key:
                    field, operator = key.split('__')
                    column = getattr(Bike, field)
                    if operator == 'gt':
                        query = query.filter(column > value)
                    elif operator == 'lt':
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
        if self.Session:
            self.Session.remove()
        if self.engine:
            self.engine.dispose()


# class DatabaseManager:
#     def __init__(self, app=None):
#         """
#         Initialize the Database Manger with optional 
#         Args:
#             app: Optional Flask application instance.
#         """
#         self.engine = None 
#         self.Session = None
#         self.logger = logging.getLogger(__name__)
#         if app is not None:
#             self.init_app(app)

#     def init_app(self, app):
#         """
#         Initialize the Database Manager with a Flask application instance.
#         """
#         @app.teardown_appcontext
#         def shutdown_session(exception=None):
#             if self.Session:
#                 self.Session.remove()

#     def init_db(self, database_url):
#         """
#         Initialize the direct database connection - use this for scripts/tasks
#         """
#         self.engine = create_engine(database_url, echo=False, pool_pre_ping=True)
#         session_factory = sessionmaker(bind=self.engine)
#         self.Session = scoped_session(session_factory)

#     @contextmanager
#     def session_scope(self):
#         """
#         Context manager for a transactional session.
#         """
#         session = self.Session()
#         try:
#             yield session
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             self.logger.error(f"Error in session: {e}")
#             raise e
#         finally:
#             session.close()
    
#     def dispose(self):
#         """
#         Dispose of the engine connection.
#         """
#         if self.engine:
#             self.engine.dispose()

#     def add_bike(self, bike):
#         """
#         Add a new bike to the database 
#         """
#         with self.session_scope() as session:
#             session.add(bike)


#     def get_all_bikes(self):
#         """
#         Fetch all bikes 
#         """
#         with self.session_scope() as session:
#             return session.query(Bike).all()
    
#     def get_all_active_bikes(self):
#         """
#         Fetch all actice bikes 
#         """
#         with self.session_scope() as session:
#             return session.query(Bike).filter_by(status='active').all()
    
#     def get_bike_by_id(self, bike_id):
#         """
#         Fetch a bike by its ID.
#         """
#         with self.session_scope() as session:
#             return session.query(Bike).filter_by(bike_id=bike_id).first()
    
#     def delete_bikes(self, bike_ids):
#         """
#         Delete bike from the database based on a list of bike IDs. 
#         """

#         if not bike_ids:
#             return # Nothing happens 
#         with self.session_scope() as session:
#             session.query(Bike).filter(Bike.bike_id.in_(bike_ids)).delete(synchronize_session=False)


#     def update_bike_maintenance(self, bike_id):
#         """
#         Update the maintenance date of a bike to today.
#         """

#         with self.session_scope() as session:
#             bike = session.query(Bike).filter_by(bike_id=bike_id).first()
#             if not bike:
#                 raise ValueError(f"Bike with ID {bike_id} does not exist.")
#             bike.last_maintenance = datetime.now().date()
 


#     def update_bike(self, bike_id, **kwargs):
#         """
#         Update the data for the bike
#         """


#         with self.session_scope() as session:
#             bike = session.query(Bike).filter_by(bike_id=bike_id).first()
#             if not bike:
#                 raise ValueError(f"Bike with ID {bike_id} does not exist.")
#             for key, value in kwargs.items():
#                 if hasattr(bike, key):
#                     setattr(bike, key, value)

#     def get_bikes_by_params(self, params):
#         """
#         Fetch bikes from the database based on dynamic parametrs

#         :param params: A dictionary containing filter conditions.
#             Example: {'status':'active', 'model_name': 'Mountain Bike'}

#             Supports operators like {'total_miles_driven__gt': 100}
#         :return: A list of Bike matching the query. 
#         """
#         with self.session_scope() as session:
#             query = session.query(Bike)
#             for key, value in params.items():
#                 if '__' in key:
#                     field, operator = key.split('__')
#                     column = getattr(Bike, field)
#                     if operator == 'gt':
#                         query = query.filter(column > value)
#                     elif operator == 'lt':
#                         query = query.filter(column < value)
#                     elif operator == 'gte':
#                         query = query.filter(column >= value)
#                     elif operator == 'lte':
#                         query = query.filter(column <= value)
#                     elif operator == 'ne':
#                         query = query.filter(column != value)
#                     elif operator == 'like':
#                         query = query.filter(column.like(f"%{value}%"))
#                 else:
#                     column = getattr(Bike, key)
#                     query = query.filter(column == value)
#             return query.all()

#     def close(self):
#         """
#         Close the session and engine connection.
#         """
#         if self.Session:
#             self.Session.remove()
#         if self.engine:
#             self.engine.dispose()
