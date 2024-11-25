import pytesseract
import PyPDF2
from pathlib import Path

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
    path = Path(file_path)
    
    if path.suffix in ('.png', '.jpg', '.jpeg'):
        return read_image(file_path)
    elif path.suffix in '.pdf':
        return read_pdf(file_path)
    else:
        return "Formato de arquivo não suportado."