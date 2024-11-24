from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       title='BB-DocScanner',
                       description='Essa documentação tem como objetivo, trazer um guia para como o endpoint estão sendo usado e para que estão sendo usado.',
                       doc='/docs'
                       )
    
    def run(self):
        self.app.run(debug=True)
        
server = Server()