import unittest 
from datetime import datetime 
from app.models import Bike 
from app.db import DatabaseManager

class TestDataBaseMananager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up an in-memory SQLite database for testing"""

        cls.db_manager = DatabaseManager(database_url='sqlite:///test_bikes.db')
        cls.db_manager.init_db()

    def setUp(self):
        """Add sample data before each test."""
        self.bike1 = Bike(
            model_name="Mountain Bike",
            purchase_date=datetime(2024, 1, 1),
            last_maintenance=datetime(2024, 2, 15),
            total_miles_driven=150.5,
            status="active"
        )
        
        self.bike2 = Bike(
            model_name="City Bike",
            purchase_date=datetime(2024, 1, 15),
            last_maintenance=datetime(2024, 2, 10),
            total_miles_driven=120.3,
            status="active"
        )
        
        self.bike3 = Bike(
            model_name="Electric Bike",
            purchase_date=datetime(2024, 2, 1),
            last_maintenance=datetime(2024, 2, 20),
            total_miles_driven=80.7,
            status="inactive"
        )
        
        self.db_manager.add_bike(self.bike1)
        self.db_manager.add_bike(self.bike2)
        self.db_manager.add_bike(self.bike3)

    def tearDown(self):
        """Clean up after each test."""
        self.db_manager.session.query(Bike).delete()
        self.db_manager.session.commit()

    @classmethod
    def tearDownClass(cls):
      """Close test db"""
      cls.db_manager.close()

    def test_get_all_active_bikes(self):
        """Test fetching all active bikes """
        bikes = self.db_manager.get_all_bikes()
        self.assertEqual(len(bikes), 2)
        self.assertTrue(all(bike.status == 'active' for bike in bikes))

    def test_get_bike_by_id(self):
        """Test getting bike by Id """

    def test_add_bike(self):
        """Test adding a bike to the database"""
        new_bike = Bike(
            model_name="Test Bike 1",
            purchase_date=datetime(2024, 3, 1),
            last_maintenance=datetime(2024, 3, 15),
            total_miles_driven=50.0,
            status="active"
        )

        self.db_manager.add_bike(new_bike)
        get_bike = self.db_manager.get_bike_by_id(new_bike.bike_id)

        self.assertIsNotNone(get_bike)

    def test_update_bike(self):
        self.db_manager.update_bike(1, status='inactive')
        updated_bike = self.db_manager.get_bike_by_id(1)
        self.assertEqual(updated_bike.status, "inactive")

    def test_update_maintenace_date(self):
        self.db_manager.update_bike_maintenance(1) # Update maintenance for bike ID 1 
        updated_bike = self.db_manager.get_all_bikes()[0]

        self.assertEqual(updated_bike.last_maintenance, datetime.now().date())

    # Now testing getting bikes by parameters 
    def test_get_bikes_by_status(self):
        """Test fetching bikes by status."""
        params = {'status': 'active'}
        bikes = self.db_manager.get_bikes_by_params(params)

        # Assert that only active bikes are returned
        self.assertEqual(len(bikes), 2)
        self.assertTrue(all(b.status == 'active' for b in bikes))

    def test_get_bikes_by_total_miles(self):
        """Test fetching bikes with total miles greater than a threshold."""
        params = {'total_miles_driven__gt': 100}
        bikes = self.db_manager.get_bikes_by_params(params)

        # Assert that only bikes with miles > 100 are returned
        self.assertEqual(len(bikes), 2)
        self.assertTrue(all(b.total_miles_driven > 100 for b in bikes))

    def test_get_bikes_by_multiple_conditions(self):
        """Test fetching bikes with multiple conditions."""
        params = {'status': 'active', 'total_miles_driven__lte': 150}
        bikes = self.db_manager.get_bikes_by_params(params)

        # Assert that only one bike matches both conditions
        self.assertEqual(len(bikes), 1)
        self.assertEqual(bikes[0].model_name, "City Bike")

    def test_get_bikes_with_like_operator(self):
        """Test fetching bikes using a LIKE operator."""
        params = {'model_name__like': 'Bike'}
        bikes = self.db_manager.get_bikes_by_params(params)

        # Assert that all bikes with "Bike" in their name are returned
        self.assertEqual(len(bikes), 3)

    def test_get_no_results(self):
        """Test fetching with parameters that yield no results."""
        params = {'status': 'inactive', 'total_miles_driven__gt': 200}
        bikes = self.db_manager.get_bikes_by_params(params)

        # Assert that no bikes match the query
        self.assertEqual(len(bikes), 0)
    
    def test_delete_bike_simple(self):
        """Test deleting a single bike by ID."""
        # Verify initial state
        bikes = self.db_manager.get_all_bikes()
        number_of_bikes = len(bikes)

        # Delete the first bike by ID 
        self.db_manager.delete_bikes([bikes[0].bike_id])


        # Verify remaining bikes
        remaining_bikes = self.db_manager.get_all_bikes()
        self.assertEqual(len(remaining_bikes),(number_of_bikes-1))  # Only one active bike should remain


if __name__ == "__main__":
    unittest.main()