from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse #importações da API
from pathlib import Path
from starlette.staticfiles import StaticFiles
import os


from resource.extration import imgToText, pdfToText

app = FastAPI() #Inicialização da API

css_directory = os.path.abspath("../css")  # Caminho para a pasta css fora de backEnd
app.mount("/css", StaticFiles(directory=css_directory), name="css")

js_directory = os.path.abspath("../Js")  # Caminho para a pasta Js fora de backEnd
app.mount("/Js", StaticFiles(directory=js_directory), name="Js")

images_directory = os.path.abspath("../Imagens")  # Caminho para a pasta imagens fora de backEnd
app.mount("/Imagens", StaticFiles(directory=images_directory), name="Imagens")

# Definir a pasta onde os arquivos vão ser guardados
UPLOAD_FOLDER = "static/files"

# Criar a pasta se não existir
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def upload_form():
    try:
        # Abrir o arquivo HTML com a codificação correta
        with open("../index.html", encoding="utf-8") as file:
            content = file.read()
            return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})
    except FileNotFoundError:
        return JSONResponse(content={"error": "HTML file not found"}, status_code=404)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Definir o caminho completo para salvar o arquivo
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Salvar o arquivo no diretório especificado
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Verificar a extensão do arquivo
    if file.filename.endswith('.pdf'):
        text = pdfToText(file_path)
        return JSONResponse(content={"text": text})
        
    elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
        # Processar a imagem enviada e extrair o texto
        text = imgToText(file_path)
        
        if text is None:
            return JSONResponse(content={"error": "Failed to read image"}, status_code=400)
        else:
            return JSONResponse(content={"text": text})
        
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

@app.get("/files/{file_name}")
def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)
