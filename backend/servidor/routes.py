from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from .app import app, db
from .modelos import Registro


@app.errorhandler(404)
def pagina_no_funciona(error):
    """ Retorna un mensaje de error al cliente """

    mensaje = {'error': error.description}

    return mensaje, 404

@app.route('/api/v1.0.0/registro/<string:dni>', methods=['GET',])
def obtener_registro(dni):
    """ Obtiene un registro según el DNI de la persona """

    registro = Registro.query.get(dni)

    if not registro:
        return abort(404, description='La persona no se encuentra en la base de datos')


    registro_serializado = {
            'id': registro.id,
            'dni': registro.dni,
            'recibo': registro.recibo,
            'nombre': registro.nombre,
            'lugar': registro.lugar,
            'inconsistencias': registro.inconsistencias
            }

    return registro_serializado
