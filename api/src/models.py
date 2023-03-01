from . import db
from .etc import anonymize_email, linear_as_int_grid

import random as r
from dataclasses import dataclass
from typing import List

def rand_uid(length: int = 7) -> str:
    """ Generates a unique id with given length. """
    alph = [chr(ordinal) for ordinal in range(97, 123)]
    num = '0123456789'
    return ''.join(r.choice(alph + list(num)) for _ in range(length))

def game_uid() -> str:
    generated = rand_uid()
    return game_uid() if Game.query.filter_by(id = generated).all() else generated

def player_uid() -> str:
    generated = rand_uid(10)
    return player_uid(10) if Player.query.filter_by(id = generated).all() else generated

# The string written below represents the game's grid as a line, to simplify the storage.
LINEAR_BASE_GRID = '0000000-0000000-0000000-0000000-0000000-0000000'

player_trophies = db.Table('player_trophies',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
    db.Column('trophy_id', db.Integer, db.ForeignKey('trophies.id'))
)

@dataclass
class Trophy(db.Model):
    __tablename__ = 'trophies'

    id: str = db.Column(db.Integer, primary_key = True)
    title: str = db.Column(db.String(50), nullable = False, unique = True)
    description: str = db.Column(db.String(256), nullable = False, unique = True)

@dataclass
class Player(db.Model):
    __tablename__ = 'players'

    id: int = db.Column(db.String(10), default = player_uid, primary_key = True)
    name: str = db.Column(db.String, default = 'Player', nullable = False, unique = True)
    email: str = db.Column(db.String, nullable = True, unique = True)
    password: str = db.Column(db.String, nullable = False)
    score: int = db.Column(db.Integer, default = 0, nullable = False)

    # FOREIGN KEY
    game_id: str = db.Column(db.String, db.ForeignKey('games.id'), nullable = True)
    
    # RELATIONSHIPS
    trophies = db.relationship('Trophy', secondary = player_trophies, backref = 'players')

    def json_repr(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'anonymized_email': anonymize_email(self.email),
            'score': self.score,
            'trophies': self.trophies,
            'current_game': self.game_id
        }

@dataclass
class Game(db.Model):
    __tablename__ = 'games'
    __allow_unmapped__ = True

    id: str = db.Column(db.String(7), default = game_uid, primary_key = True)
    matrix: str = db.Column(db.String(47), default = LINEAR_BASE_GRID, nullable = False)
    turn: int = db.Column(db.Integer, default = 1, nullable = False)

    # RELATIONSHIP
    players: List[Player] = db.relationship('Player', backref = 'game', lazy = True)

    def json_repr(self) -> dict:
        return {
            'id': self.id,
            'matrix': linear_as_int_grid(self.matrix),
            'turn': self.turn,
            'players': self.players
        }