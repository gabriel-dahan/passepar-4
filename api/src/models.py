from . import db
from .etc import anonymize_email, linear_as_int_grid, rand_uid
from .auth import AuthTokens

from dataclasses import dataclass
from typing import List
from datetime import datetime

def game_uid() -> str:
    generated = rand_uid()
    return game_uid() if Game.query.filter_by(id = generated).all() else generated

def user_uid() -> str:
    generated = rand_uid(10)
    return user_uid(10) if User.query.filter_by(id = generated).all() else generated

# The string written below represents the game's grid as a line, to simplify the storage.
LINEAR_BASE_GRID = '0000000-0000000-0000000-0000000-0000000-0000000'

@dataclass
class Player(db.Model):
    __tablename__ = 'players'
    __allow_unmapped__ = True

    id: int = db.Column(db.Integer, primary_key = True)
    color: int = db.Column(db.Integer, nullable = False)

    # FOREIGN KEY
    user_id: str = db.Column(db.String, db.ForeignKey('users.id'))
    game_id: str = db.Column(db.String, db.ForeignKey('games.id'), nullable = False)

    def json_repr(self) -> dict:
        return {
            'id': self.id,
            'color': self.color,
            'user_id': self.user_id,
            'game_id': self.game_id
        }

@dataclass
class Game(db.Model):
    __tablename__ = 'games'
    __allow_unmapped__ = True

    id: str = db.Column(db.String(7), default = game_uid, primary_key = True)
    matrix: str = db.Column(db.String(47), default = LINEAR_BASE_GRID, nullable = False)
    turn: int = db.Column(db.Integer, default = 1, nullable = False)
    status: int = db.Column(db.Integer, default = 0, nullable = False) # 1 if game started else 0 
    created_at: datetime = db.Column(db.DateTime, default = datetime.now(), nullable = False)
    public: bool = db.Column(db.Boolean, nullable = False)
    created_by: bool = db.Column(db.String, db.ForeignKey('users.id'), nullable = False, unique = True)

    # RELATIONSHIP
    players: List[Player] = db.relationship('Player', backref = 'game', lazy = True)

    def json_repr(self) -> dict:
        return {
            'id': self.id,
            'matrix': linear_as_int_grid(self.matrix),
            'turn': self.turn,
            'players': self.players,
            'status': self.status,
            'created_at': self.created_at,
            'public': self.public,
            'owner': self.owner.json_repr()
        }
    
@dataclass
class User(db.Model):
    __tablename__ = 'users'
    __allow_unmapped__ = True

    id: int = db.Column(db.String(10), default = user_uid, primary_key = True)
    name: str = db.Column(db.String, nullable = False, unique = True)
    email: str = db.Column(db.String, nullable = True, unique = True)
    avatar_url: str = db.Column(db.String, nullable = False)
    password: str = db.Column(db.String, nullable = False)
    score: int = db.Column(db.Integer, default = 0, nullable = False)

    # RELATIONSHIPS
    auth_tokens: List[AuthTokens] = db.relationship('AuthTokens', backref = 'user', lazy = True) # One-to-Many
    player: Player = db.relationship('Player', backref = 'user', lazy = True, uselist = False) # One-to-One
    owner_of: Game = db.relationship('Game', backref = 'owner', lazy = True, uselist = False) # One-to-One

    def json_repr(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'email': self.email,
            'anonymized_email': anonymize_email(self.email),
            'score': self.score,
            'auth_tokens': self.auth_tokens
        }