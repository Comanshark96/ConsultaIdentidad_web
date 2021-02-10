import os
from flask import Flask, jsonify
from modelos import Registro

app = Flask(__name__)

# CONFIGURACIÓN DE LA BASE DE DATOS
BASE_DIR = os.path.abspath(os.getcwd())
DB_DIR = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_DIR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/api/1.0.0/registro/<int:id>', methods=['GET',])
def obtener_registro(id):
    """ Obtiene un registro según el ID """

    registro = Registro.query.filter(id=id).first()
    registro_serializado = jsonify(registro)

    return registro_serializado
