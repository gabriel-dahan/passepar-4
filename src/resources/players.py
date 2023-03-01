from flask import jsonify
from flask_restful import Resource, request, reqparse
from werkzeug.security import generate_password_hash
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

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, required = True, location = 'form')
        self.parser.add_argument('email', type = str, required = True, location = 'form')
        self.parser.add_argument('password', type = str, required = True, location = 'form')

    def post(self):
        args = self.parser.parse_args()
        name = args.get('name')
        email = args.get('email')
        password = args.get('password')
        if player := Player.query.filter((Player.name == name) | (Player.email == email)).first():
            if player.email == email:
                return jsonify({
                    'code': 'P1-1',
                    'message': 'Player\'s email is already registered.'
                })
            return jsonify({
                'code': 'P1-2',
                'message': 'Player\'s name already exists.'
            })
        p = Player(
            name = name,
            email = email,
            password = generate_password_hash(password)
        )
        db.session.add(p)
        db.session.commit()

        return jsonify({
            'message': f'Player \'{p.id}\' was successfuly registered.'
        })

# -- RESOURCES -- #
root = '/api/players'
api.add_resource(PlayerUpdate, f'{root}/<string:playerid>/update')
api.add_resource(PlayerInfo, f'{root}/<string:playerid>/')
api.add_resource(NewPlayer, f'{root}/register')