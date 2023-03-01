from flask import jsonify, Response
from flask_restful import Resource, request, reqparse

from .. import api, db
from ..models import Game, Player
from ..core import GameCore
from ..etc import linear_as_int_grid, int_grid_as_linear

# --- GAME API --- #

class AddPlayer(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('player_id', type = str, required = True, location = 'form')

    def post(self, gamekey: str) -> Response:
        args = self.parser.parse_args()
        player_id = args.get('player_id')
        player: Player = Player.query.filter_by(id = player_id).first()
        if not player:
            return jsonify({
                'code': 'G4',
                'message': f'Player with id \'{player_id}\' doesn\'t exist.'
            })
        game: Game = Game.query.filter_by(id = gamekey).first()
        if len(game.players) >= 2:
            return jsonify({
                'code': 'G1',
                'message': 'The maximum number of players has already been reached.'
            })
        if player.game_id:
            return jsonify({
                'code': 'G5',
                'message': f'Player \'{player.id}\' is already in \'{player.game_id}\'.'
            })
        game.players.append(player)
        db.session.commit()
        return jsonify({
            'message': f'Player \'{player.id}\' was successfuly added to game \'{game.id}\'.'
        })

class GameChange(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('column', type = int, required = True, location = 'form')

    def put(self, gamekey: str):
        game = Game.query.filter_by(id = gamekey).first()
        args = self.parser.parse_args()
        column = args.get('column')
        if column < 0 or column > 6:
            return jsonify({
                'code': 'G6',
                'message': f'The choosen column must be between 0 and 6 (column : {column}).'
            })
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        
        matrix_transform = linear_as_int_grid(game.matrix)
        c4 = GameCore(array = matrix_transform)
        line = c4.get_y_pos(column)
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

class GamesList(Resource):
    
    def get(self):
        args = request.args
        __only_ids = args.get('onlyids')
        only_ids = __only_ids == 'True' or not __only_ids
        if only_ids:
            return jsonify({
                'games': [g.id for g in Game.query.all()]
            })
        return jsonify({
            'games': 
                [{'id': g.id, 'matrix': linear_as_int_grid(g.matrix)} for g in Game.query.all()]
        })

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
api.add_resource(GameChange, f'{root}/<string:gamekey>/play')
api.add_resource(GameDeletion, f'{root}/<string:gamekey>/delete')
api.add_resource(GameInfo, f'{root}/<string:gamekey>')
api.add_resource(GamesList, f'{root}/list')
api.add_resource(NewGame, f'{root}/new')