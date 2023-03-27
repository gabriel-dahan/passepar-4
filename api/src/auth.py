from . import db

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
    
def generate_uuid() -> str:
    return str(uuid4())

@dataclass
class AuthTokens(db.Model):
    __tablename__ = 'auth_tokens'

    token: str = db.Column(db.String, default = generate_uuid, primary_key = True)
    logged_on: datetime = db.Column(db.DateTime, default = datetime.now, nullable = False)
    period: int = db.Column(db.Integer, nullable = True) # In seconds

    # FOREIGN KEY
    user_id: str = db.Column(db.String, db.ForeignKey('users.id'), nullable = False)

    def json_repr(self) -> dict:
        return {
            'token': self.token,
            'logged_on': self.logged_on,
            'period': self.period,
            'user': self.user
        }