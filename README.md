INSTALAR .VENV:
Caso a venv esteja previamente instalada no projeto, delete-a e crie uma na sua maquina.

python -m venv .venv - Serve para criar uma venv 

.\.venv\Scripts\activate - Serve para ativar a venv, utilize esse codigo para fazer as aplicações funcionarem

pip install flask pytesseract PyPDF2 spacy - Instalar as dependencias

python -m spacy download pt_core_news_sm - Para ficar em português

python -m spacy validate - Verificar a instalação

#rodar a aplicação python app.py

INSTALAÇÕES NECESSARIAS:

#instalar o Pillow  
pip install pdf2image Pillow

#instalar o PyMuPDF 
pip install PyMuPDF

#pip install pandas scikit-learn joblib

#pip install apache-airflow

#pip install spacy-lookups-data

------------------------------------------------------------------------------------------------------------------------------------------------------------------

COMO FUNCIONA:

Envio de Arquivos: O usuário envia um arquivo (imagem ou PDF) junto com uma consulta na área de texto (por exemplo: "nome", "valor", "cpf").
Processamento do Documento: O sistema usa pytesseract para imagens e PyPDF2 para PDFs para extrair o texto do arquivo enviado.

Busca de Informações: O texto extraído é analisado, e o sistema busca padrões baseados na consulta do usuário. Ele reconhece nomes, CPF/CNPJ, valores, datas, identificadores e chaves vinculadas, separando pagador e recebedor.

Resposta Personalizada: Com base no que o usuário solicita, ele retorna apenas as informações pertinentes, como nomes, CPF/CNPJ, etc.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

COMO USAR:

Se o usuário solicitar "todos os nomes": Ele retornará tanto o nome do pagador quanto do recebedor.

Se o usuário solicitar "nome de quem recebeu" ou "nome de quem pagou": Apenas o nome do pagador será exibido.

Se o usuário solicitar "valor": O valor da transação será retornado.

Se o usuário solicitar "cpf" ou "cnpj": Os CPFs/CNPJs do pagador e do recebedor serão retornados.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

ESTRUTURA DE PASTAS:

NÃO MEXEM POR CONTA PROPRIA, POIS PODE GERAR PROBLEMAS.

.venv - Configurações da API e deve aparecer quando fazer as instalações que tá no topo (aparece sozinha).

static
    |_ Css
    |_ Js
    |_ Imagens

são usadas paras as pastas de estilo, animações e imagens.

Templates
    |_Index.html - Pagina inicial html
    |_Result.html- Pagina onde exibe os resultados

Uploads - Pasta onde ficaram os arquivos enviados para API, um armazenamento temporario.

app.py - nossa API e seu codigo de funcionamento, DEVE FICAR FORA DE QUALQUER PASTA!.