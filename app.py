from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

# Inicializando a aplicação Flask
app = Flask(__name__)

# Definindo a pasta para uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Criando a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Rota para a página principal que exibe o formulário
@app.route('/')
def home():
    return render_template('index.html')

# Rota para servir arquivos estáticos
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Rota de upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'message' not in request.form:
        return 'Nenhum arquivo ou mensagem fornecido.', 400

    file = request.files['file']
    message = request.form['message']

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Realizar OCR no arquivo
        extracted_text = process_file(file_path)

        # Filtrar a informação baseada na mensagem do usuário
        requested_info = search_information(extracted_text, message)

        # Exibir o resultado em outra página HTML
        return render_template('result.html', result=requested_info)

if __name__ == '__main__':
    app.run(debug=True)
