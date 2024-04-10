from flask import Flask
from flask_jwt_extended import JWTManager
from peewee import Database
from config import Config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'abcdnicolas1234'
db = Database(app)
jwt = JWTManager(app)

from app import routes, models
