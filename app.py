from flask import Flask, request, render_template, send_from_directory
import pytesseract
import PyPDF2
from werkzeug.utils import secure_filename
import os
import re
import spacy

# Inicializando a aplicação Flask
app = Flask(__name__)

# Definindo a pasta para uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Criando a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Carregando o modelo de linguagem da spaCy
nlp = spacy.load("pt_core_news_sm")

# Rota para a página principal que exibe o formulário
@app.route('/')
def home():
    return render_template('index.html')

# Rota para servir arquivos estáticos
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Função para ler imagens com Tesseract
def read_image(file_path):
    return pytesseract.image_to_string(file_path)

# Função para ler PDFs com PyPDF2
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# Função principal para processar arquivos
def process_file(file_path):
    if file_path.endswith(('.png', '.jpg', '.jpeg')):
        return read_image(file_path)
    elif file_path.endswith('.pdf'):
        return read_pdf(file_path)
    else:
        return "Formato de arquivo não suportado."

# Função para buscar informações no texto extraído
def search_information(extracted_text, query):
    results = []  # Lista para armazenar todas as informações encontradas

    # Normalizando o texto para facilitar a busca
    extracted_text = extracted_text.lower()

    # Busca por informações do pagador ou recebedor com base na consulta
    if "nome de quem pagou" in query.lower() or "quem pagou" in query.lower():
        name_payer = re.findall(r'nome:\s*(.*)', extracted_text)
        if name_payer:
            results.append(f"Nome do Pagador: {name_payer[0].strip()}")  # Primeiro nome encontrado
    elif "nome de quem recebeu" in query.lower() or "quem recebeu" in query.lower():
        name_receiver = re.findall(r'nome:\s*(.*)', extracted_text)
        if name_receiver:
            results.append(f"Nome do Recebedor: {name_receiver[-1].strip()}")  # Último nome encontrado
    elif "todos os nomes" in query.lower():  # Se o usuário pedir apenas "nome"
        names = re.findall(r'nome:\s*(.*)', extracted_text)
        if names:
            # Caso o usuário não especifique, retorna tanto o pagador quanto o recebedor
            results.append(f"Nome do Pagador: {names[0].strip()}")
            results.append(f"Nome do Recebedor: {names[-1].strip()}")

    # Busca por CNPJ
    if "cnpj" in query.lower():
        cnpj_match = re.findall(r'cnpj / cpf:\s*(\S+)', extracted_text)
        if cnpj_match:
            results.append(f"CNPJ: {cnpj_match[0]}")

    # Busca por número da nota fiscal
    if "número da nota" in query.lower() or "número nf" in query.lower():
        nf_number = re.findall(r'nf-e\s*nº\.\s*(\S+)', extracted_text)
        if nf_number:
            results.append(f"Número da Nota Fiscal: {nf_number[0]}")

    # Busca por valor
    if "valor" in query.lower():
        value = re.findall(r'valor total:\s*r\$\s?(\d+,\d{2})', extracted_text)
        if value:
            results.append(f"Valor Total: R$ {value[0]}")

    # Busca por data de emissão
    if "data de emissão" in query.lower():
        emission_date = re.findall(r'data da emissão\s*(\d{2}/\d{2}/\d{4})', extracted_text)
        if emission_date:
            results.append(f"Data de Emissão: {emission_date[0]}")

    # Busca por destinatário (Nome e Endereço)
    if "destinatário" in query.lower():
        recipient_name = re.findall(r'destinatário:\s*(.*?)(?=\s*-)', extracted_text)
        recipient_address = re.findall(r'endereço\s*(.*?)(?=\s*cep)', extracted_text)
        if recipient_name and recipient_address:
            results.append(f"Destinatário: {recipient_name[0].strip()}")
            results.append(f"Endereço: {recipient_address[0].strip()}")

    # Busca por forma de pagamento
    if "forma de pagamento" in query.lower():
        payment_method = re.findall(r'forma de pagamento\s*:\s*(\S+)', extracted_text)
        if payment_method:
            results.append(f"Forma de Pagamento: {payment_method[0]}")

    # Busca por chave de acesso
    if "chave de acesso" in query.lower():
        access_key = re.findall(r'chave de acesso\s*(\S+)', extracted_text)
        if access_key:
            results.append(f"Chave de Acesso: {access_key[0]}")

    # Busca por informações complementares
    if "informações complementares" in query.lower():
        additional_info = re.findall(r'informações complementares\s*([\s\S]+)', extracted_text)
        if additional_info:
            results.append(f"Informações Complementares: {additional_info[0].strip()}")

    # Retornar as informações encontradas
    if not results:
        return "Não foi possível encontrar as informações solicitadas."

    return ", ".join(results)

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
