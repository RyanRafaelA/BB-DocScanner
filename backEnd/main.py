from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from pathlib import Path
import os
import cv2

from resource.extration import imgToText, pdfToText

app = FastAPI()

# Definir a pasta onde os arquivos vão ser guardados
UPLOAD_FOLDER = "static/files"

# Criar a pasta se não existir
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def upload_form():
    try:
        # Página de onde puxamos os arquivos
        with open("../frontEnd/index.html") as file:  
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
        text = pdfToText(file_path)
        
        return JSONResponse(content={"text": text})
        
    elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
        # Abrir a imagem usando OpenCV (cv2.imread) a partir do arquivo salvo, e mandando para o metodo imgToText()
        text = imgToText(cv2.imread(file_path))
        
        if text is None:
            return JSONResponse(content={"error": "Failed to read image"}, status_code=400)
        else:
            return JSONResponse(content={"text": text})
        
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

@app.get("/files/{file_name}")  # Servir arquivo carregado (imagem ou PDF)
def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)