from flask import jsonify
from flask_restful import Resource

from . import api, db
from .models import Game

# --- RESTAPI --- #

class GameAPI(Resource):
    def get(self, gamekey):
        return jsonify({
            'key': gamekey
        })

    def post(self, gamekey):
        return self.get(gamekey)

class NewGameAPI(Resource):
    def get(self):
        return jsonify({
            'message': 'A POST request must be executed at this endpoint.'
        })

    def post(self):
        new_game = Game()
        db.session.add(new_game)
        db.session.commit()
        print(Game.query.all())
        return jsonify({
            'game_id': new_game.id,
            'message': f'The game \'{new_game.id}\' was successfuly created.'
        })

# -- RESOURCES -- #
root = '/game/api'
api.add_resource(GameAPI, f'{root}/<string:gamekey>/')
api.add_resource(NewGameAPI, f'{root}/new')