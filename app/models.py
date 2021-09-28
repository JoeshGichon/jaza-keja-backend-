from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'User {self.name}'