import logging
from Logger import create_app
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask, request


app = create_app('Logger')
app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(usuarioID)s - %(ip)s - %(token)s')

file_handler = logging.FileHandler('logAlarmas.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

alarmasLog = Flask(__name__)

class VistaLogger(Resource):
    def post(self):
        usuarioID=request.json["usuarioID"]
        ip=request.remote_addr
        token=request.json["token"]
        data = {
            "usuarioID" : usuarioID,
            "ip" : ip,
            "token" : token
        }
        return logger.info('', extra=data)


api.add_resource(VistaLogger, '/logger')
