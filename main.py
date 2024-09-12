from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import os
from pathlib import Path

app = FastAPI()

#pra acessar a imagem usa a porta http://127.0.0.1:8000/
#para rodar a aplicação - uvicorn nome do arquivo:app

UPLOAD_FOLDER = "static/files" # <- Pasta onde os arquivos vão ser guardados
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def upload_form():
    with open("frontEnd/index.html") as file: # <- Página de onde puxamos os arquivos
        return file.read()


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)): # <- Processamento de arquivos para upload
    file_extension = file.filename.split(".")[-1]
    

    if file_extension not in ["png", "jpg", "jpeg", "pdf"]:     # <- Verifica se os arquivos são validos
        return {"error": "File format not supported!"}
    
    
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"  # <- Salva o arquivo
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    

    return RedirectResponse(url=f"/files/{file.filename}", status_code=302)  # Redireciona automaticamente a imagem do arquivo sem precisar colocar a porta manualmente


@app.get("/files/{file_name}")  # < - Servir arquivo carregado (imagem ou PDF)
def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

