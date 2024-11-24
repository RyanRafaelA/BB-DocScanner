from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server

app = server.app
api = server.api

@api.route('/teste')
class HelloWorld(Resource):
    def get(self):
        return 'Hello World'