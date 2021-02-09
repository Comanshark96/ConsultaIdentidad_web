import os
from flask import Flask

app = Flask(__name__)


# CONFIGURACIÓN DE LA BASE DE DATOS
BASE_DIR = os.path.abspath(os.getcwd())
DB_DIR = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_DIR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def inicio():
    return 'Hola mundo'
