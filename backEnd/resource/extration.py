import fitz  # pymupdf é importado como fitz
import pytesseract
import cv2
import shutil
import concurrent.futures
import numpy as np

def configure_tesseract():
    # Verifica se o Tesseract está instalado e disponível no sistema
    tesseract_cmd = shutil.which("tesseract")
    if tesseract_cmd is None:
        raise EnvironmentError("Tesseract OCR não encontrado. Certifique-se de que ele está instalado e no PATH do sistema.")
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def imgToText(file_path):
    # Abrir a imagem usando OpenCV (cv2.imread) a partir do caminho do arquivo
    image = cv2.imread(file_path)
    
    if image is None:
        return None

    # Aplicar OCR usando pytesseract
    return pytesseract.image_to_string(image, config="--psm 6")

def pdfToText(file_path):
    doc = fitz.open(file_path)
    text = ""

    # Processar cada página do PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extrair e tratar o texto da página
        page_text = page.get_text("text").encode("utf8").decode("utf8")     # Extraindo o texto da página
        page_text = page_text.replace("\n", " ")                            # Remover quebras de linha
        page_text = page_text.strip()                                       # Remover espaços em branco
        
        # Adicionar quebra de linha dupla para separar as páginas
        text += page_text + "\n\n"
        
        # Adicionar o texto extraído de imagens, se houver
        text += imgInAPdf(page)

    # Remover múltiplas quebras de linha consecutivas e manter apenas uma
    formatted_text = " ".join([line for line in text.splitlines() if line.strip()])

    return formatted_text


def imgInAPdf(page):
    text = ""
    image_list = page.get_images(full=True)

    for img in image_list:
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Convertendo os bytes da imagem em uma matriz do NumPy
        image_np_array = np.frombuffer(image_bytes, np.uint8)
        
        # Decodificar a imagem em memória usando o OpenCV
        image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)
        
        if image is not None:
            # Realizar OCR na imagem
            text += pytesseract.image_to_string(image, config="--psm 6")

    return text
