from . import db

import random as r

def uid(length: int = 7) -> str:
    """ Generates a unique id with given length. """
    alph = [chr(ordinal) for ordinal in range(97, 123)]
    num = '0123456789'
    generated = ''.join(r.choice(alph + list(num)) for _ in range(length))
    if Game.query.filter_by(id = generated).all():
        return uid(length)
    return generated

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String, nullable = False)
    name = db.Column(db.String, default = 'Player', nullable = False)

    # FOREIGN KEY
    game_id = db.Column(db.String, db.ForeignKey('games.id'), nullable = False)

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.String(7), default = uid, primary_key = True)
    # The string written below represents the game's set as a line, to simplify the storage.
    matrix = db.Column(db.String(47), default = '0000000-0000000-0000000-0000000-0000000-0000000', nullable = False)
    turn = db.Column(db.Integer, default = 1)

    # RELATIONSHIP
    players = db.relationship('Player', backref = 'game', lazy = True)