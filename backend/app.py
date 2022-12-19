from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS # Remove during deployment

from api.HelloApiHandler import HelloApiHandler
from api.CSTRController import CSTRAdiabaticApiHandler

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/home')
api.add_resource(CSTRAdiabaticApiHandler, '/cstr/adiabatic')