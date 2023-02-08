from core import Power4

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values

CONF = dotenv_values('.env')

__app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
__app.url_map.strict_slashes = False

__app.config['SECRET'] = CONF['SECRET']

# --- DATABASE --- #
__app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
__app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
__db = SQLAlchemy(__app)

# --- ROUTES --- #

@__app.route('/api/game/<key:str>')
def game(key: str):
    return 

if __name__ == '__main__':
    __app.run(debug = True)