import fitz  # pymupdf é importado como fitz
import pytesseract
import cv2
import shutil

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
    text = ""
    
    # Abrindo o arquivo PDF com PyMuPDF
    doc = fitz.open(file_path)
    
    # Para cada página do PDF, extrair texto
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extrair imagens da página e processar com OCR, se necessário
        text += imgInAPdf(page)

        # Extrair o texto direto da página (sem imagens)
        page_text = page.get_text("text").encode("utf8").decode("utf8")
        page_text = page_text.replace("\n", " ").strip()
        text += page_text + "\n\n"  # Separar páginas com quebras de linha duplas

    # Remover múltiplas quebras de linha consecutivas e manter apenas uma
    formatted_text = "\n".join([line for line in text.splitlines() if line.strip()])

    return formatted_text

def imgInAPdf(page):
    text = ""
    image_list = page.get_images(full=True)
    
    for img in image_list:
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_bytes = base_image["image"]
        image_filename = f"temp_img_{xref}.png"
        
        # Salvar a imagem extraída temporariamente
        with open(image_filename, "wb") as image_file:
            image_file.write(image_bytes)
        
        # Realizar OCR na imagem
        text += imgToText(image_filename)
    
    return text
