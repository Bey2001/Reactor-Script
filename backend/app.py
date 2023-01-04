from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # Remove during deployment

from api.CSTRController import CSTRAdiabaticApiHandler, CSTRHeatExchangerApiHandler, CSTRSpacetimeApiHandler, CSTRTempApiHandler, CSTRVarCoApiHandler

from api.PFRController import PFRAdiabaticApiHandler, PFRSpacetimeApiHandler, PFRTempApiHandler, PFRVarCoApiHandler

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)

api.add_resource(CSTRAdiabaticApiHandler, '/cstr/adiabatic')
api.add_resource(CSTRHeatExchangerApiHandler, '/cstr/exchanger')
api.add_resource(CSTRSpacetimeApiHandler, '/cstr/spacetime')
api.add_resource(CSTRTempApiHandler, '/cstr/temp')
api.add_resource(CSTRVarCoApiHandler, '/cstr/varco')
api.add_resource(PFRAdiabaticApiHandler, '/pfr/adiabatic')
api.add_resource(PFRSpacetimeApiHandler, '/pfr/spacetime')
api.add_resource(PFRTempApiHandler, '/pfr/temp')
api.add_resource(PFRVarCoApiHandler, '/pfr/varco')
