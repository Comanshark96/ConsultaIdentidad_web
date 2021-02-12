import os

BASE_DIR = os.path.abspath(os.getcwd())
DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')

class Config:
    """ Configuración base de la aplicación """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "LaLlaveMasSecreta"

class ConfigProduccion(Config):
    """ Configuración de la aplicación en producción """

    SECRET_KEY = os.environ['SECRET_KEY']

class ConfigDesarrollo(Config):
    """ Configuración de la aplicación en desarrollo """

    DEBUG = True
