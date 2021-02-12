from .app import db

# DEFINIENDO BASE DE DATOS

class Registro(db.Model):
    """ Identifica un registro de una persona en el RNP """

    dni = db.Column(db.String(15), primary_key=True)
    recibo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    lugar = db.Column(db.String(50), unique=True, nullable=False)
    inconsistencias = db.Column(db.Integer, unique=True, nullable=False)
