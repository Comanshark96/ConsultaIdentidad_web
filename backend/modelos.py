from flask_sqlalchemy import SQLAlchemy
from app import app


# DEFINIENDO BASE DE DATOS
db = SQLAlchemy(app)

class Registro(db.Model):
    """ Identifica un registro de una persona en el RNP """

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(15), unique=True, nullable=False)
    recibo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    lugar = db.Column(db.String(50), unique=True, nullable=False)
    inconsistencias = db.Column(db.Integer, unique=True, nullable=False)

if __name__ == '__main__':
    db.create_all()
