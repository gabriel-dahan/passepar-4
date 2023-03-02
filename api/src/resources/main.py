from flask import jsonify
from flask_restful import Resource

from . import API_ROOT
from .. import api

# --- GENERAL API --- #

class API(Resource):

    def get(self):
        return jsonify({
            'api': 'Connect4 - API',
            'version': 'v0.1[beta]',
            'authors': [
                'Gabriel DAHAN'
            ]
        })

# -- RESOURCES -- #
api.add_resource(API, f'{API_ROOT}')