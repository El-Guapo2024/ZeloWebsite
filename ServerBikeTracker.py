from flask import Flask, render_template, jsonify 
from datetime import datetime
import random 
import folium 
from markupsafe import Markup
app = Flask(__name__)
# TODO
# In-memory storage for bike data (replace with database in a real application 


def generate_fake_data():
    bikes = {}
    for i in range(1,6):
        bikes[f"bike_{i}"] = {
            "latitude" : round(random.uniform(40.0, 41.0), 6),      
            "longitude": round(random.uniform(-74.0, -73.0), 6),
            "speed": round(random.uniform(0, 30), 1),
            "timestamp": (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
    return bikes

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/get_bikes')
def get_bikes():
    bikes = generate_fake_data()
    return render_template('bikes_table.html', bikes=bikes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

