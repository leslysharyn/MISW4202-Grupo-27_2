import logging
import Authenticator
from Logger import create_app
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask, request
from .modelo import db, Usuario

app = create_app('Logger')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Authenticator/authenticator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('Timestamp: %(asctime)s - usuarioID: %(usuarioID)s - Direccion: %(ip)s - Token: %(token)s - llave privada: %(skey)s')

file_handler = logging.FileHandler('logAlarmas.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

alarmasLog = Flask(__name__)

port = 3000

class VistaLogger(Resource):
    def post(self):
        usuarioID=request.json["usuarioID"]
        ip=request.remote_addr
        skey=request.json["skey"]
        usuario = Usuario.query.filter(Usuario.id == usuarioID).first()
        token=request.json["token"]
        data = {
            "usuarioID" : usuarioID,
            "ip" : ip,
            "token" : token,
            "skey" : skey
        }
        logger.info('', extra=data)
        if usuario.skey == skey:
            return {"message": "Log Creado"}, 200
        else:
            return {"message": "Alerta usuario no autorizado"}, 404


api.add_resource(VistaLogger, '/logger')
