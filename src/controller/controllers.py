from flask import Flask, request
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
import os

from src.server.instance import server
from src.ocr.extract import process_file
from src.service.logic import search_information

app = server.app
api = server.api

# Definindo a pasta para uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Criando a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
document = api.parser()
document.add_argument('file', type=FileStorage, location='files', required=True)
document.add_argument('message', type=str, location='form', required=True)

#O endpoint que vai receber um arquivo e uma mensagem.
@api.route('/scan', endpoint='scanner')
class Scan(Resource):
    @api.expect(document, validate=True)
    @api.doc(
        params={
            'file': {'description':'Arquivo que vai ser analisado'},
            'message': {'description':'O que vai ser encontrado no arquivo'}
        },
        body={
            'example':{
                'file': './uploads/1727552647248.pdf',
                'message': 'Nome do Recebedor'
            }
        }
    )
    def post(self):
        if 'file' not in request.files or 'message' not in request.form:
            return 'Nenhum chave file ou message foi fornecido.', 400

        file = request.files['file']
        message = request.form['message']
        
        if message == '' or file.filename == '':
            return 'Nenhuma mensagem e arquivo foi enviada.', 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Realizar OCR no arquivo
            extracted_text = process_file(file_path)
            
            if extracted_text == '':
                return 'Arquivo em branco.', 400
            
            # Filtrar a informação baseada na mensagem do usuário
            requested_info = search_information(extracted_text, message)

            # Exibir o resultado
            return {'result' : requested_info}, 200