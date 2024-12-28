from flask import (
    Blueprint,render_template, request,
    current_app, jsonify, make_response
)
from app.models import Bike
from app.db import DatabaseManager
from datetime import datetime
from app.utils import get_selected_bikes_to_json
# Create a Blueprint for bike-related routes
bike_routes = Blueprint('bike_routes', __name__)
db_manager = DatabaseManager(database_url='sqlite:///bikes.db')

selected_bikes = []
is_filter_on = False 
# Home Page Routes 
@bike_routes.route('/')
def index():
    """
    Initial Home Page Start
    Will Load Bike List
    """
    bikes = db_manager.get_all_bikes()
    return render_template('index.html', bikes=bikes)

@bike_routes.route('/bikes/list')
def get_bike_list():
    """
    Return only the bike list as partial template
    """
    bikes = db_manager.get_all_bikes()
    return render_template('partials/index/bikes_list.html', bikes=bikes)

@bike_routes.route('/bikes/<int:bike_id>/edit_form', methods=['GET'])
def edit_bike(bike_id):
    """Fetch the edit form for a specific bike."""
    bike = db_manager.get_bike_by_id(bike_id)
    if not bike:
        return render_template('error.html', message=f'Bike with ID {bike_id} not found'), 404
    return render_template('/partials/index/edit_bike_form.html', bike=bike)

@bike_routes.route('/bikes/<int:bike_id>/update_maintenance', methods=['POST'])
def update_bike_maintenance(bike_id):
    """Update_bike maintenance date to today"""
    db_manager.update_bike_maintenance(bike_id)
    # For now we return an empty response 
    # in the future we can better behaviour here
    response = make_response("", 200) 
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response

## Bike Form 
@bike_routes.route('/bikes/<int:bike_id>/update', methods=['POST'])
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

    response = make_response("", 200) 
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response

@bike_routes.route('/bikes/<int:bike_id>/delete', methods=['DELETE'])
def delete_bike(bike_id):
    "Delete Specific bike"

    db_manager.delete_bikes([bike_id])

    # Empty the div on delete and HX-Trigger header
    response = make_response("", 200)
    response.headers['HX-Trigger'] = 'refreshBikeList'
    return response
 
#Add Page Form
@bike_routes.route('/bikes/add', methods=['GET'])
def get_bikes_add():
    """Render the intiaal Add Bike form."""
    return render_template('add_bike.html')

@bike_routes.route('/bikes/add_form', methods=['POST'])
def post_bikes_add_form():
    """Add a new bike, and reload form"""
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
    # Return a HTML response with HX-Trigger header
    response = make_response(render_template('partials/add_bike/add_bike_form.html'), 200)
    return response

# Search Page with Map Routes 
@bike_routes.route('/bikes/bike_map', methods=['GET'])
def get_bike_map():
    """Search bikes based on parameters."""
    bikes = db_manager.get_all_bikes()
    return render_template('bike_map.html', bikes=bikes)

@bike_routes.route('/bikes/select_bikes', methods=['POST'])
def select_bikes():

    data = request.form.getlist("selected_bike")
    current_app.cache_manager.set_selected_bikes(data)
    current_app.cache_manager.set_active_searching(True)
    response = make_response(render_template("partials/bike_map/bubble.html"), 200)
    response.headers['HX-Trigger'] = 'activateMap'
    return response

@bike_routes.route('/bikes/update_markers', methods=['GET'])
def update_markers():
    """Update the markers on the map."""
    is_active_searching = current_app.cache_manager.get_active_searching()
    print("Getting Selected Bikes")
    if not is_active_searching:
        return jsonify([])
    shared_data = current_app.mqtt_subscriber.get_shared_data()
    selected_bikes = current_app.cache_manager.get_selected_bikes()
    return get_selected_bikes_to_json(shared_data, selected_bikes)

@bike_routes.route('/bikes/deselect_bikes', methods=['POST'])
def deselect_bikes():
    """Deselect bikes."""
    current_app.cache_manager.set_selected_bikes([])
    current_app.cache_manager.set_active_searching(False)
    response = make_response('', 200)
    response.headers['HX-Trigger'] = 'deactivateMap'
    return response
    
 