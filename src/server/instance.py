from flask import Flask
from flask_restx import Api
from flask_cors import CORS

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       title='BB-DocScanner',
                       description='Esta documentação tem como objetivo apresentar um guia detalhado sobre a utilização do endpoint, explicando seu propósito e funcionamento. O sistema permite o envio de arquivos e retorna as informações extraídas de seu conteúdo.',
                       doc='/docs'
                       )
    
    def run(self):
        CORS(self.app)
        self.app.run(debug=True)
        
server = Server()