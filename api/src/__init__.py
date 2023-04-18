from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

from dotenv import dotenv_values

CONF = dotenv_values('.env')

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
cors = CORS(app, resources = {r'/api/*': {'origins': '*'}}) # Allows CORS
# Initialize RESTful API & SocketIO websocket server.
api = Api(app)
socket = SocketIO(
    app, 
    path = '/websocket',
    cors_allowed_origins = '*'
)
scheduler = APScheduler()

app.url_map.strict_slashes = False

app.config['SECRET'] = CONF['SECRET']
app.config['BUNDLE_ERRORS'] = True

# --- DATABASE --- #
app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from src.resources import main, games, users