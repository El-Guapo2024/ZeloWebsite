from app.utils import generate_fake_location_data
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from app.models import Bike
from app.db import DatabaseManager
from app import app
from datetime import datetime
db_manager = DatabaseManager(database_url='sqlite:///bikes.db')

query = None 
@app.route('/')
def index():
    """Homepage"""
    print("We are in the first entry point")
    bikes = db_manager.get_all_bikes()
    return render_template('bikes.html', bikes=bikes)

@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    """Get all bikes"""
    bikes = db_manager.get_all_bikes()
    return render_template('/partials/_bikes_partial.html', bikes=bikes)

@app.route('/bikes/<int:bike_id>', methods=['GET'])
def get_bike_by_id(bike_id):
    """Get a bike by its ID."""
    bike = db_manager.get_bike_by_id(bike_id)
    if not bike:
        return render_template('error.html', message=f'Bike with ID {bike_id} not found'), 404
    return render_template('/partials/_bike_detail_partial.html', bike=bike)

@app.route('/bikes/add', methods=['GET'])
def get_bikes_add():
    """Render the Add Bike form."""
    return render_template('add_bike.html')

@app.route('/bikes/add', methods=['POST'])
def post_bikes_add():
    """Add a new bike."""
    data = request.form

    # Create a new Bike instance with form data
    new_bike = Bike(
        model_name=data['model_name'],
        purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date(),
        last_maintenance=datetime.strptime(data.get('last_maintenance'),'%Y-%m-%d'),
        total_miles_driven=float(data.get('total_miles_driven', 0)),
        status=data['status']
    )
    # Add and commit new bike to the database
    db_manager.add_bike(new_bike)
    # Return a JSON response with HX-Trigger header
    response = jsonify(success=True)
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response


@app.route('/bikes/<int:bike_id>/edit', methods=['POST'])
def update_bike_old(bike_id):
    """Update a bike's details."""
    data = request.form

    try:
        db_manager.update_bike(bike_id, **data)
        update_bike = db_manager.get_bike_by_id(bike_id)
        return render_template('/partials/_bike_detail_partial.html', bike=update_bike)
    except ValueError as e:
        return render_template('error.html', message=str(e)), 400
    

@app.route('/bikes/<int:bike_id>/maintenance', methods=['POST'])
def update_bike_maintenance(bike_id):
    """Update_bike maintenance date to today"""
    
    db_manager.update_bike_maintenance(bike_id)
    response = jsonify(success=True)
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response

@app.route('/bikes/delete', methods=['POST'])
def delete_bikes():
    data = request.form 
    if not data or 'bike_ids' not in data:
        return render_template('error.html', message="Missing bike_ids field"), 400
    
    bike_ids = list(map(int, data.getlist('bike_ids')))
    db_manager.delete(bike_ids)
    bikes = db_manager.get_all_bikes()
    return render_template('/partials/_bikes_partial.html', bikes)

@app.route('/bikes/search', methods=['POST'])
def get_bike_by_params():
    """Search bikes based on parameters."""
    params = request.form.to_dict()
    bikes = db_manager.get_bikes_by_params(params)
    return render_template('/partials/_search_results_partial.html', bikes=bikes)
    
@app.route('/bikes/<int:bike_id>/edit', methods=['GET'])
def edit_bike(bike_id):
    """Fetch the edit form for a specific bike."""
    bike = db_manager.get_bike_by_id(bike_id)

    if not bike:
        return render_template('error.html', message=f'Bike with ID {bike_id} not found'), 404
    
    return render_template('/partials/_edit_bike_form.html', bike=bike)

@app.route('/bikes/<int:bike_id>/update', methods=['POST'])
def update_bike(bike_id):
    """Update a specific bike's details."""
    data = request.form
    db_manager.update_bike(
        bike_id=bike_id,
        model_name=data['model_name'],
        purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d'),
        last_maintenance=datetime.strptime(data.get('last_maintenance'),'%Y-%m-%d'),
        total_miles_driven=float(data.get('total_miles_driven')),
        status=data['status']
    )

    response = jsonify(success=True)
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response

@app.route('/bikes/<int:bike_id>/delete', methods=['DELETE'])
def delete_bike(bike_id):
    "Delete Specific bike"

    db_manager.delete_bikes([bike_id])

    # Create a response with an empty div and HX-Trigger header
    response = make_response('<div></div>', 200)
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response
 