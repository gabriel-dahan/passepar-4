from flask import jsonify
from flask_restful import Resource, request
from typing import List

from . import api, db
from .models import Game, Player
from .core import Power4

def linear_as_int_grid(linear_grid: str) -> List[List[int]]:
    return [[int(elem) for elem in line] for line in linear_grid.split('-')]
    
def int_grid_as_linear(int_grid: List[List[int]]) -> str:
    res = ''
    for line in int_grid:
        res += ''.join(str(elem) for elem in line)
        res += '-'
    return res[:-1]

"""
ERR. CODES : 
    - 1 : invalid coordinates
    - 2 : game doesn't exist
    - 3 : no space left on the choosen column
    - 4 : a POST request must be executed
    - 5 : max number of players reached
"""

# --- GAME API --- #

class AddPlayer(Resource):

    def post(self, gamekey: str):
        args = request.args
        ip = args.get('ip')
        name = args.get('name')
        game = Game.query.filter_by(id = gamekey).first()
        if len(game.players) >= 2:
            return jsonify({
                'code': 5,
                'message': 'The maximum number of players has already been reached.'
            })
        p = Player(ip = ip, name = name, game_id = gamekey)
        db.session.add(p)
        db.session.commit()
        return jsonify({
            'message': f'Player {p.name} was successfuly added.'
        })

class GameChange(Resource):

    def put(self, gamekey: str):
        game = Game.query.filter_by(id = gamekey).first()
        args = request.args
        column = int(args.get('column'))
        if not game:
            return jsonify({
                'code': 2,
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        matrix_transform = linear_as_int_grid(game.matrix)
        p4 = Power4(array = matrix_transform)
        line = p4.get_y_axis(column)
        if line == -1:
            return jsonify({
                'code': 3,
                'message': 'No space is left on this column.'
            })
        matrix_transform[line][column] = game.turn
        game.matrix = int_grid_as_linear(matrix_transform)
        game.turn = game.turn % 2 + 1 # Returns 1 or 2 - the modulo basically switches players from 1 to 2 or from 2 to 1 for the next round.
        db.session.commit()
        return jsonify({
            'message': 'The game was successfuly updated.'
        })

class GameInfo(Resource):
    def get(self, gamekey: str):
        game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 2,
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        return jsonify(game)

    def post(self, gamekey: str):
        return self.get(gamekey)

class NewGame(Resource):
    def get(self):
        return jsonify({
            'code': 4,
            'message': 'A POST request must be executed at this endpoint.'
        })

    def post(self):
        new_game = Game()
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            'game_id': new_game.id,
            'message': f'Game \'{new_game.id}\' was successfuly created.'
        })

# -- RESOURCES -- #
root = '/api/game'
api.add_resource(AddPlayer, f'{root}/<string:gamekey>/addplayer')
api.add_resource(GameChange, f'{root}/<string:gamekey>/update')
api.add_resource(GameInfo, f'{root}/<string:gamekey>/')
api.add_resource(NewGame, f'{root}/new')