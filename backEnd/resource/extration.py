import pymupdf
import pytesseract

def configure_tesseract():
    # Verifica se está instalado e disponível no sistema
    tesseract_cmd = shutil.which("tesseract")
    if tesseract_cmd is None:
        raise EnvironmentError("Tesseract OCR não encontrado. Certifique-se de que ele está instalado e no PATH do sistema.")
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
def imgToText(file_path):
    # Abrir a imagem usando OpenCV (cv2.imread) a partir do arquivo salvo
    image = cv2.imread(file_path)
    
    if image is None:
        return None

    # Aplicar OCR usando pytesseract
    return pytesseract.image_to_string(image, config="--psm 6")
    
def pdfToText(file_path):
    text = ""
    
    #abrindo o arquivo pelo pymupdf
    doc = pymupdf.open(file_path)
    
    #depois que abriu o pdf e transformando em texto
    for page in doc:
        page_text = page.get_text("text").encode("utf8").decode("utf8")     # Extraindo o texto da página
        page_text = page_text.replace("\n", " ")                            # Removendo o \n da resposta
        page_text = page_text.strip()                                       # Removendo os espacos em branco
        text += page_text + "\n\n"                                          # Quebra de linha dupla para separar as paginas
        
    # Remover múltiplas quebras de linha consecutivas e manter apenas uma
    formatted_text = "\n".join([line for line in text.splitlines() if line.strip()])

    return formatted_text

def imgInAPdf(page):
    text = ""
    
    image = page.get_images() # extraindo imagem de uma pagina pdf
    text = imgToText(image) # enviando para o imgToText(), que vai trasnforma a imagem
    
    return text