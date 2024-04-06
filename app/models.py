from app import db
from peewee import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password_hash = CharField()

    class Meta:
        database = db

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @property
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    