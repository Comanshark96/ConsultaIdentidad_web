from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config


app = Flask(__name__)
app.config.from_object(config.ConfigDesarrollo)
db = SQLAlchemy(app)

from .routes import obtener_registro
