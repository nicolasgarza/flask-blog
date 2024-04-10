from app import db
from peewee import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    username = CharField(unique=True)
    password_hash = CharField()

    class Meta:
        database = db

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @property
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    
class Post(db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    author = ForeignKeyField(User, backref='posts')
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = db

class Comment(db.Model):
    post = ForeignKeyField(Post, backref='comments')
    author = ForeignKeyField(User, backref='comments')
    slug = CharField(unique=True)
    content = TextField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = db