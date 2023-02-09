from . import db

import random as r
from dataclasses import dataclass
from typing import List

def uid(length: int = 7) -> str:
    """ Generates a unique id with given length. """
    alph = [chr(ordinal) for ordinal in range(97, 123)]
    num = '0123456789'
    generated = ''.join(r.choice(alph + list(num)) for _ in range(length))
    if Game.query.filter_by(id = generated).all():
        return uid(length)
    return generated

# The string written below represents the game's grid as a line, to simplify the storage.
LINEAR_BASE_GRID = '0000000-0000000-0000000-0000000-0000000-0000000'

@dataclass
class Player(db.Model):
    __tablename__ = 'players'

    id: int = db.Column(db.Integer, primary_key = True)
    ip: str = db.Column(db.String, nullable = False)
    name: str = db.Column(db.String, default = 'Player', nullable = False)

    # FOREIGN KEY
    game_id: str = db.Column(db.String, db.ForeignKey('games.id'), nullable = False)

@dataclass
class Game(db.Model):
    __tablename__ = 'games'
    __allow_unmapped__ = True

    id: str = db.Column(db.String(7), default = uid, primary_key = True)
    matrix: str = db.Column(db.String(47), default = LINEAR_BASE_GRID, nullable = False)
    turn: int = db.Column(db.Integer, default = 1)

    # RELATIONSHIP
    players: List[Player] = db.relationship('Player', backref = 'game', lazy = True)