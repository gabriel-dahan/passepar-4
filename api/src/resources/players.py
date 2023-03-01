from flask import jsonify, Response
from flask_restful import Resource, request, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

from .. import api, db
from ..models import Player
from ..etc import anonymize_email

# --- PLAYERS API --- #

class PlayerUpdate(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, location = 'form')
        self.parser.add_argument('email', type = str, location = 'form')
        self.parser.add_argument('password', type = str, location = 'form')

    def put(self, playerid: str) -> Response:
        player: Player = Player.query.filter_by(id = playerid).first()
        if not player:
            return jsonify({
                'code': 'P2',
                'message': f'Player with id \'{playerid}\' doesn\'t exist.'
            })
        args = self.parser.parse_args()
        for key, val in args.items():
            if not val:
                continue
            if key == 'password':
                player.password = generate_password_hash(v)
                continue
            setattr(player, key, val)
        db.session.commit()
        return jsonify({
            'message': f'Player \'{player.id}\' was successfuly updated.'
        })

class PlayerInfo(Resource):

    def get(self, playerid: str) -> Response:
        p: Player = Player.query.filter_by(id = playerid).first()
        if not p:
            return jsonify({
                'code': 'P2',
                'message': f'Player with id \'{playerid}\' doesn\'t exist.'
            })
        return jsonify({
            'id': p.id,
            'name': p.name,
            'email': p.email,
            'anonymized_email': anonymize_email(p.email)
        })

class LoginPlayer(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type = str, required = True, location = 'form')
        self.parser.add_argument('password', type = str, required = True, location = 'form')

    def post(self) -> Response:
        args = self.parser.parse_args()
        player: Player = Player.query.filter_by(email = args['email']).first()
        if not player:
            return jsonify({
                'code': 'P2',
                'message': f'Player with email \'{args["email"]}\' doesn\'t exist.'
            })
        valid = check_password_hash(player.password, args['password'])
        if not valid:
            return jsonify({
                'code': 'P4',
                'message': f'Login failed, incorrect password for the user \'{player.id}\'.'
            })
        
        # --> Cookie storing TODO

        return jsonify({
            'message': f'Player \'{player.id}\' was successfuly logged in.'
        })

class RegisterPlayer(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, required = True, location = 'form')
        self.parser.add_argument('email', type = str, required = True, location = 'form')
        self.parser.add_argument('password', type = str, required = True, location = 'form')

    def post(self) -> Response:
        args = self.parser.parse_args()
        name = args.get('name')
        email = args.get('email')
        password = args.get('password')
        try:
            v = validate_email(email)
        except EmailNotValidError as e:
            return jsonify({
                'code': 'P3',
                'message': f'Email \'{email}\' is not valid.',
                'human_readable': str(e)
            })
        email = v['email'] # Replaced with normalized form.
        if player := Player.query.filter((Player.name == name) | (Player.email == email)).first():
            if player.email == email:
                return jsonify({
                    'code': 'P1',
                    'subcode': '1',
                    'message': 'Player\'s email is already registered.'
                })
            return jsonify({
                'code': 'P1',
                'subcode': '2',
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
root = '/api/player'
api.add_resource(PlayerUpdate, f'{root}/<string:playerid>/update')
api.add_resource(PlayerInfo, f'{root}/<string:playerid>/')
api.add_resource(LoginPlayer, f'{root}/login')
api.add_resource(RegisterPlayer, f'{root}/register')