
# Back - End

...
## Rodando o projeto

Para rodar o projeto, rode o seguinte comando:

```bash
  uvicorn main:app --reload
```
## Instalação

O FastApi, é para rodar nossa api.
```bash
  pip install fastapi uvicorn
```

O PyTesseract, que transforma arquivos do tipo imagem em texto.
```bash
  pip install pytesseract
```
Tambem é necessario instalar utilizando o executavel do tesseract em: https://github.com/UB-Mannheim/tesseract/wiki

O OpenCV, serve para abrir o arquivo, auxiliando o pytesseract.
```bash
  pip install opencv-python
```

O PyMuPDF, vai ler o arquivo do tipo pdf.
```bash
  pip install pymupdf
```