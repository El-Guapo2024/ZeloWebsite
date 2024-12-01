from app import app , db
from app.utils import generate_fake_location_data
from flask import render_template, request, jsonify 
import os 

@app.route('/')
def index():
    bikes = db.get_all_bikes()
    print("Get bikes ")
    print(os.getcwd())
    return render_template('./templates/index.html', bikes=bikes)

@app.route('/get_bikes')
def get_bikes():
    selected_bike_ids = request.args.getlist('bikes[]')
    if selected_bike_ids:
        bikes = [db.get_bike(int(bike_id)) for bike_id in selected_bike_ids]
    else:
        bikes = db.get_all_bikes()
    
    bike_data = generate_fake_location_data(bikes)
    return render_template('/templates/bikes_table.html', bike_data)


