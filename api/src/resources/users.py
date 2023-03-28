from flask import jsonify, Response
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

from . import API_ROOT
from .. import api, db
from ..models import User, AuthTokens
from ..etc import generate_avatar_url

from typing import List

# --- USERS API --- #

class UserUpdate(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, location = 'form')
        self.parser.add_argument('email', type = str, location = 'form')
        self.parser.add_argument('password', type = str, location = 'form')
        self.parser.add_argument('score', type = int, location = 'form')

    def put(self, userid: str) -> Response:
        user: User = User.query.filter_by(id = userid).first()
        if not user:
            return jsonify({
                'code': 'U2',
                'message': f'User with id \'{userid}\' doesn\'t exist.'
            })
        args = self.parser.parse_args()
        for key, val in args.items():
            if not val:
                continue
            if key == 'password':
                user.password = generate_password_hash(val)
                continue
            setattr(user, key, val)
        db.session.commit()
        return jsonify({
            'message': f'user \'{user.id}\' was successfuly updated.',
            'user': user.json_repr()
        })

class SearchUser(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type = str, default = '', location = 'args')
        self.parser.add_argument('email', type = str, default = '', location = 'args')
        self.parser.add_argument('limit', type = int, default = 10, location = 'args')

    def get(self) -> Response:
        args = self.parser.parse_args()
        if args['limit'] > 100:
            return jsonify({
                'code': 'U5',
                'message': 'User search limit cannot be greater than 100.'
            })
        matches: List[User] = User.query.filter(
            (User.name.like(f"%{args['name']}%")) | (User.email.like(f"%{args['email']}%"))
        ).limit(args['limit']).all()
        return jsonify({'users': [user.json_repr() for user in matches]})
    
class UserInfo(Resource):

    def get(self, userid: str) -> Response:
        u: User = User.query.filter_by(id = userid).first()
        if not u:
            return jsonify({
                'code': 'U2',
                'message': f'User with id \'{userid}\' doesn\'t exist.'
            })
        return jsonify(u.json_repr())

class LoginUser(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type = str, required = True, location = 'form')
        self.parser.add_argument('password', type = str, required = True, location = 'form')

    def post(self) -> Response:
        args = self.parser.parse_args()
        user: User = User.query.filter_by(email = args['email']).first()
        if not user:
            return jsonify({
                'code': 'U2',
                'message': f'User with email \'{args["email"]}\' doesn\'t exist.'
            })
        valid = check_password_hash(user.password, args['password'])
        if not valid:
            return jsonify({
                'code': 'U4',
                'message': f'Login failed, incorrect password for the user \'{user.id}\'.'
            })
        
        auth = AuthTokens(user = user)
        db.session.add(auth)
        db.session.commit()

        return jsonify({
            'message': f'User \'{user.id}\' was successfuly logged in.',
            'user': user.json_repr(),
            'auth_token': auth.token
        })

class RegisterUser(Resource):

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
                'code': 'U3',
                'message': f'Email \'{email}\' is not valid.',
                'human_readable': str(e)
            })
        email = v['email'] # Replaced with normalized form.
        if user := User.query.filter((User.name == name) | (User.email == email)).first():
            if user.email == email:
                return jsonify({
                    'code': 'U1',
                    'subcode': 'S1',
                    'message': 'This email already exists in the database.'
                })
            return jsonify({
                'code': 'U1',
                'subcode': 'S2',
                'message': 'This name is already taken.'
            })
        u = User(
            name = name,
            email = email,
            avatar_url = generate_avatar_url(email),
            password = generate_password_hash(password)
        )
        db.session.add(u)
        db.session.commit()

        return jsonify({
            'message': f'User \'{u.id}\' was successfully registered.',
            'user': u.json_repr()
        })
    

### TOKENS RELATIVE

class GetUserSession(Resource):

    def get(self, sessiontoken: str) -> Response:
        t: AuthTokens = AuthTokens.query.filter_by(token = sessiontoken).first()
        u: User = t.user
        if not u:
            return jsonify({
                'code': 'U6',
                'message': f'Session token \'{sessiontoken}\' is no longer valid.'
            })
        return jsonify(u.json_repr())

class DeleteUserSession(Resource):

    def delete(self, sessiontoken: str):
        session: AuthTokens = AuthTokens.query.filter_by(token = sessiontoken).first()
        if not session:
            return jsonify({
                'code': 'U6',
                'message': f'Session with token \'{sessiontoken}\' does not exist.'
            })
        db.session.delete(session)
        db.session.commit()
        return jsonify({
            'message': f'Session with token \'{session.token}\' was successfuly deleted.',
            'session': session.json_repr()
        })

# -- RESOURCES -- #
root = f'{API_ROOT}/user'
api.add_resource(UserUpdate, f'{root}/<string:userid>/update')
api.add_resource(UserInfo, f'{root}/<string:userid>')
api.add_resource(LoginUser, f'{root}/login')
api.add_resource(RegisterUser, f'{root}/register')
api.add_resource(SearchUser, f'{root}/search')
api.add_resource(GetUserSession, f'{root}/token/<string:sessiontoken>')
api.add_resource(DeleteUserSession, f'{root}/token/<string:sessiontoken>/delete')