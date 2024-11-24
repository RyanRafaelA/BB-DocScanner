from flask import Flask, request
from flask_restx import Api, Resource
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

@api.route('/scan')
class Scan(Resource):
    def post(self):
        if 'file' not in request.files or 'message' not in request.form:
            return 'Nenhum arquivo ou mensagem fornecido.', 400

        file = request.files['file']
        message = request.form['message']

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.name)
            file.save(file_path)

            # Realizar OCR no arquivo
            extracted_text = process_file(file_path)

            # Filtrar a informação baseada na mensagem do usuário
            requested_info = search_information(extracted_text, message)

            # Exibir o resultado
            return requested_info, 200