from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            title='BB-DocScanner',
            description='Esta documentação tem como objetivo apresentar um guia detalhado sobre a utilização do endpoint, explicando seu propósito e funcionamento. O sistema permite o envio de arquivos e retorna as informações extraídas de seu conteúdo.',
            doc='/docs'
        )
        # Configuração para produção
        self.app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

    def run(self):
        CORS(self.app)
        port = int(os.environ.get("PORT", 5000))  # Porta definida pelo Render ou 5000
        self.app.run(host="0.0.0.0", port=port)   # Ativando para produção
        
server = Server()
