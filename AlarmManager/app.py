from Alarm1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import json
from urllib import response
import urllib3
import secrets

app = create_app('AlarmManager')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)
failsService = True

port=4000
forceAtack = False

urlAuth = 'http://127.0.0.1:5000/login'
urlLogger = 'http://127.0.0.1:3000/logger'
class VistaAlarmLogin(Resource):

    def post(self): 
        jsonVar = json.dumps(request.json)
        userData = self.login(jsonVar)
        logerData = self.logger(userData)
        if logerData["message"] == 'Log Creado':
            return {"message": 'AlarmaProcesada'},200 
        else: 
            return {"message": 'No se puede procesar la alarma por autenticación'},404 

    def login(self, jsonData):
        http = urllib3.PoolManager()
        req = http.request('POST', urlAuth, headers={'Content-Type': 'application/json'}, body=jsonData)
        userData = json.loads(req.data)
        return userData
    
    def logger(self, jsonData):
        http = urllib3.PoolManager()
        skey = jsonData["skey"]
        if forceAtack:
            skey = secrets.token_hex(16)
        body = {
            'usuarioID': jsonData["usuario_id"],
            'skey': skey,
            'token': jsonData["token"],
        }
        newBody = json.dumps(body)
        req = http.request('POST', urlLogger, headers={'Content-Type': 'application/json'}, body=newBody)
        loggerData = json.loads(req.data)
        return loggerData

api.add_resource(VistaAlarmLogin, '/login')
