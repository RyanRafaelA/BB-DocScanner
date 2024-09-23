import pymupdf
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\py-libs\\Tesseract-OCR\\Tesseract.exe"

def imgToText(image):
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