from flask import jsonify, Response
from flask_restful import Resource, request, reqparse

from typing import Union

from .. import api, db
from ..models import Game, Player, User
from ..core import GameCore
from ..etc import linear_as_int_grid, int_grid_as_linear

# --- GAME API --- #

class AddPlayer(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type = str, default = None, location = 'form')
        self.parser.add_argument('color', type = int, required = True, location = 'form')

    def post(self, gamekey: str) -> Response:
        args = self.parser.parse_args()
        user_id = args.get('user_id')
        color = args.get('color')

        game: Game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        if len(game.players) >= 2:
            return jsonify({
                'code': 'G1',
                'message': 'The maximum number of players has already been reached.'
            })
        
        if user_id:
            user: User = User.query.filter_by(id = user_id).first()
            if not user:
                return jsonify({
                    'code': 'G4',
                    'message': f'User \'{user_id}\' does not exist.'
                })
            if user.player:
                return jsonify({
                    'code': 'G5',
                    'message': f'User \'{user.id}\' is already in \'{user.player.game_id}\'.'
                })
        
        player = Player(
            user_id = user_id,
            game_id = game.id,
            color = color
        )
        
        db.session.add(player)
        game.players.append(player)
        db.session.commit()
        return jsonify({
            'message': f'Player \'{user_id}\' was successfuly added to game \'{game.id}\'.'
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
        game: Game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        db.session.delete(game)
        db.session.commit()
        return jsonify({
            'message': f'The game with id \'{gamekey}\' was successfuly deleted.',
            'game': game.json_repr()
        })

class GameInfo(Resource):

    def get(self, gamekey: str):
        game: Game = Game.query.filter_by(id = gamekey).first()
        if not game:
            return jsonify({
                'code': 'G2',
                'message': f'Game with id \'{gamekey}\' does not exist.'
            })
        return jsonify(game.json_repr())

class GamesList(Resource):
    
    def get(self):
        args = request.args
        __only_ids = args.get('only_ids')
        only_ids = __only_ids.lower() == 'true' if __only_ids else False
        if only_ids:
            return jsonify({
                'games': [g.id for g in Game.query.all()]
            })
        __only_public = args.get('only_public')
        only_public = __only_public.lower() == 'true' if __only_public else False
        return jsonify({
            'games': 
                [g.json_repr() for g in Game.query.all() if g.public] if only_public else [g.json_repr() for g in Game.query.all()]
        })

class NewGame(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('public', type = bool, default = False, location = 'form')

    def post(self):
        args = self.parser.parse_args()
        public = args.get('public')
        new_game = Game(public = public)
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            'message': f'Game \'{new_game.id}\' was successfuly created.',
            'game': new_game.json_repr()
        })

# -- RESOURCES -- #
root = '/api/game'
api.add_resource(AddPlayer, f'{root}/<string:gamekey>/addplayer')
api.add_resource(GameChange, f'{root}/<string:gamekey>/play')
api.add_resource(GameDeletion, f'{root}/<string:gamekey>/delete')
api.add_resource(GameInfo, f'{root}/<string:gamekey>')
api.add_resource(GamesList, f'{root}/list')
api.add_resource(NewGame, f'{root}/new')