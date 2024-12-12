from flask import Flask
from flask_htmx import HTMX 

app = Flask(__name__)

htmx = HTMX(app)

from app import routes, models

