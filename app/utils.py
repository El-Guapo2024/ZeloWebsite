
def get_selected_bikes_to_json(shared_bikes_dict, selected_bikes):
    """Get selected bikes from the form."""
    # Convert to bike ID = "Bike"+bike_id
    selected_bikes = [f"Bike{bike_id}" for bike_id in selected_bikes]
    print(selected_bikes)
    print(shared_bikes_dict)

    markers = []
    for bike_id in selected_bikes:
        if bike_id in shared_bikes_dict:
            bike_data = shared_bikes_dict[bike_id]
            markers.append({
                "lat": bike_data.latitude,
                "lng": bike_data.longitude,
                "popup": f"""
                    <b>Bike ID:</b> {bike_id}<br>
                    <b>Speed:</b> {bike_data.speed} km/h<br>
                    <b>Timestamp:</b> {bike_data.timestamp}<br>
                    <b>Satellites:</b> {bike_data.satellites}
                """
            })

    return markers
