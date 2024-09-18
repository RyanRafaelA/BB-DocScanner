from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from PIL import Image
import pytesseract
import io
from pathlib import Path
import cv2
import os

app = FastAPI()

# Pasta onde os arquivos vão ser guardados
UPLOAD_FOLDER = "static/files"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = "C:\\py-libs\\Tesseract-OCR\\Tesseract.exe"


@app.get("/", response_class=HTMLResponse)
def upload_form():
    try:
        with open("frontEnd/index.html") as file:  # Página de onde puxamos os arquivos
            return file.read()
    except FileNotFoundError:
        return JSONResponse(content={"error": "HTML file not found"}, status_code=404)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Definir o caminho completo para salvar o arquivo
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Ler o arquivo enviado
    contents = await file.read()

    # Salvar o arquivo no diretório especificado
    with open(file_path, "wb") as f:
        f.write(contents)

    # Verificar a extensão do arquivo
    if file.filename.endswith('.pdf'):
        return JSONResponse(content={"error": "PDF handling not implemented"})
    elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
        # Abrir a imagem usando PIL
        image = cv2.imread(io.BytesIO(contents))

        # Aplicar OCR usando pytesseract
        text = pytesseract.image_to_string(image, config="--psm 6")

        return JSONResponse(content={"text": text})
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)


@app.get("/files/{file_name}")  # Servir arquivo carregado (imagem ou PDF)
def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)
