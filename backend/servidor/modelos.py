from .app import db

# DEFINIENDO BASE DE DATOS

class Registro(db.Model):
    """ Identifica un registro de una persona en el RNP """

    dni = db.Column(db.String(13), primary_key=True)
    recibo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    lugar = db.Column(db.String(50), nullable=False)
    inconsistencias = db.Column(db.Integer, nullable=False)
