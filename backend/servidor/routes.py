from flask import abort, request
from sqlalchemy.exc import SQLAlchemyError
from .app import app, db
from .modelos import Registro
from .ConsultaIdentidad import ConsultaIdentidad as Buscar

def serializar_registro(registro):
    """ Serializa un registro de la base de datos """

    registro_serializado = {
            'dni': registro.dni,
            'recibo': registro.recibo,
            'nombre': registro.nombre,
            'lugar': registro.lugar,
            'inconsistencias': registro.inconsistencias
            }

    return registro_serializado


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

    return serializar_registro(registro)


@app.route('/api/v1.0.0/registro', methods=['POST'])
def crear_registro():
    """ Genera un nuevo registro a partir de la página del RNP """

    busqueda = request.json['identidad']

    rnp_registro = Buscar(busqueda)

    if not rnp_registro.encontrado:
        return abort(404, description='La persona no se encuentra en la base de datos del RNP')

    nuevo_registro = Registro(dni=rnp_registro.identidad,
            recibo=rnp_registro.recibo,
            nombre=rnp_registro.nombre,
            lugar=rnp_registro.lugar,
            inconsistencias=rnp_registro.inconcistencias)

    db.session.add(nuevo_registro)
    db.session.commit()

    return serializar_registro(nuevo_registro)
