import sqlite3 
from datetime import datetime 
import sys 

def init_db():
    print("\n === Starting Database Initialization ===",flush=True)
    try: 
        print('1. Connecting to database ...')
        conn = sqlite3.connect('bikes.db')
        cursor = conn.cursor()
        print(" ✓ Connected successfully")
        # Create Bikes table 
        print("\n2. Creating Bikes table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bikes (
            bike_id INTEGER PRIMARY KEY, 
            model_name VARCHAR(50),
            purchase_date DATE,
            last_maintenance DATE,
            total_miles_driven FLOAT,
            status VARCHAR(20)                      
        )
        ''')
            # Create sample data if table is empty

        conn.commit() # Commit table to creation first 
        print("   ✓ Table created/verified")

        print("\n3. Checking if table is empty...")
        cursor.execute('SELECT COUNT(*) FROM Bikes')
        count = cursor.fetchone()[0]
        print(f"   ✓ Current bike count: {count}")
        if count == 0:
            print("\n4. Inserting sample data...")
            sample_bikes = [
                ('Mountain Bike 1', '2024-01-01', '2024-02-15', 150.5, 'active'),
                ('City Bike 1', '2024-01-15', '2024-02-10', 120.3, 'active'),
                ('Electric Bike 1', '2024-02-01', '2024-02-20', 80.7, 'active')
            ]
            cursor.executemany('''
                INSERT INTO Bikes (model_name, purchase_date, last_maintenance, total_miles_driven, status)
                VALUES (?, ?, ?, ?, ?)
            ''', sample_bikes)

            conn.commit()
            print("   ✓ Sample data inserted")
        print("\n=== Database Initialization Complete ===")
    except Exception as e :
        print(f"\n❌ ERROR: {str(e)}")
        print(f"Error Type: {type(e).__name__}")
        raise e
    finally:
        conn.close()
        print("\nDatabase connection closed")

def get_db():
    conn = sqlite3.connect('bikes.db')
    conn.row_factory = sqlite3.Row

    return conn 

def get_all_bikes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bikes WHERE status = "active"')
    bikes = cursor.fetchall()
    conn.close()
    return bikes 

def get_bike(bike_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bikes WHERE bike_id = ?',(bike_id,))
    bike = cursor.fetchone()
    conn.close()
    return bike 

def update_bike_maintenance(bike_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Bikes
        SET last_maintenance = ? 
        WHERE bike_id = ? 
''',(datetime.now().strftime('%Y-%m-%d'), bike_id))
    
    conn.commit()
    conn.close()