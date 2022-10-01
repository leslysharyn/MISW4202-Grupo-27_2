from Alarm1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json


app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)
failsService = True

class VistaAlarm(Resource):

    def post(sefl): 
        urlBase = 'http://127.0.0.1:5000/login'
        usuario= (request.json["usuario"], request.json["contrasena"])
        r = requests.post(urlBase, usuario)
       
        print(r.status_code, r.reason)       
        
        if r.status_code == 404: 
            return  r.json
        else: 
            return r.json

    def get(self):
            return {
                "result": "alarma procesada",
            }, 200


api.add_resource(VistaAlarm, '/alarm')
