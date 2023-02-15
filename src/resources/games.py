from flask import jsonify
from flask_restful import Resource, request
from typing import List

from .. import api, db
from ..models import Game, Player
from ..core import GameCore

def linear_as_int_grid(linear_grid: str) -> List[List[int]]:
    return [[int(elem) for elem in line] for line in linear_grid.split('-')]
    
def int_grid_as_linear(int_grid: List[List[int]]) -> str:
    res = ''
    for line in int_grid:
        res += ''.join(str(elem) for elem in line)
        res += '-'
    return res[:-1]

# --- GAME API --- #

class AddPlayer(Resource):

    def post(self, gamekey: str):
        args = request.args
        ip = args.get('ip')
        name = args.get('name')
        game = Game.query.filter_by(id = gamekey).first()
        if len(game.players) >= 2:
            return jsonify({
                'code': 'G1',
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
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        
        matrix_transform = linear_as_int_grid(game.matrix)
        p4 = GameCore(array = matrix_transform)
        line = p4.get_y_pos(column)
        if line == -1:
            return jsonify({
                'code': 'G3',
                'message': 'No space is left on this column.'
            })
        matrix_transform[line][column] = game.turn
        game.matrix = int_grid_as_linear(matrix_transform)
        game.turn = game.turn % 2 + 1 # Returns 1 or 2 - the modulo basically switches players from 1 to 2 or from 2 to 1 for the next round.
        db.session.commit()
        return jsonify({
            'message': 'The game was successfuly updated.'
        })

class GameDeletion(Resource):

    def delete(self, gamekey: str):
        game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        db.session.delete(game)
        db.session.commit()
        return jsonify({
            'message': f'The game with id \'{gamekey}\' was successfuly deleted.'
        })

class GameInfo(Resource):
    
    def get(self, gamekey: str):
        game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        return jsonify({
            'id': game.id,
            'matrix': linear_as_int_grid(game.matrix),
            'players': game.players,
            'turn': game.turn
        })

    def post(self, gamekey: str):
        return self.get(gamekey)

class GamesList(Resource):
    
    def get(self):
        return jsonify(Game.query.all())

class NewGame(Resource):

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
api.add_resource(GameDeletion, f'{root}/<string:gamekey>/delete')
api.add_resource(GameInfo, f'{root}/<string:gamekey>/')
api.add_resource(GamesList, f'{root}/list')
api.add_resource(NewGame, f'{root}/new')