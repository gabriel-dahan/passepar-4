from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from dotenv import dotenv_values

CONF = dotenv_values('.env')

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
api = Api(app)

app.url_map.strict_slashes = False

app.config['SECRET'] = CONF['SECRET']

# --- DATABASE --- #
app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from src.core import Power4
from src import resources