from app import app

@app.route('/')
def index():
    return  render_template('index.html')


@app.route('/get_all_bikes')
def get_bikes():
    bikes = get_bike_data()
    return render_template('bikes_table.html', bikes=bikes)

@app.route('/get_bike_by_id')
def get_bike_by_id():
    
