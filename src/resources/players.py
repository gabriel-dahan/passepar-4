from flask import jsonify
from flask_restful import Resource, request
from typing import List

from .. import api, db
from ..models import Game, Player


# --- PLAYERS API --- #

class PlayerUpdate(Resource):

    def put(self, playerid: str):
        pass

class PlayerInfo(Resource):

    def get(self, playerid: str):
        pass

class NewPlayer(Resource):

    def post(self):
        pass

# -- RESOURCES -- #
root = '/api/players'
api.add_resource(PlayerUpdate, f'{root}/<string:playerid>/update')
api.add_resource(PlayerInfo, f'{root}/<string:playerid>/')
api.add_resource(NewPlayer, f'{root}/register')