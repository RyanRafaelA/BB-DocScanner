import spacy
from spacy.training.example import Example
import random
from spacy.lang.pt import Portuguese
from spacy.lookups import Lookups

# Carrega o modelo em português
nlp = Portuguese()
lookups = Lookups()
lookups.add_table("lexeme_norm", {})
nlp.vocab.lookups.add_table("lexeme_norm", lookups.get_table("lexeme_norm"))

# Define o conjunto de dados de treinamento
TRAIN_DATA = [
    ("Nome do pagador é João da Silva e o CPF é 123.456.789-00", 
     {"entities": [(17, 29, "PAGADOR"), (39, 53, "CPF")]}),
    (
        "RECEBEMOS DE ITA PECAS PARA VEICULOS COMERCIO E SERVICOS LTDA OS PRODUTOS E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL "
        "ELETRÔNICA INDICADA ABAIXO. EMISSÃO: 17/05/2024 VALOR TOTAL: R$ 630,56 DESTINATÁRIO: VALTER MARQUES SANTOS - "
        "RUA ARICURI LOTE 3, 32 SETOR HAB JARDIM BOTANICO BRASILIA-DF", 
        {
            "entities": [
                (13, 55, "EMITENTE"),
                (93, 103, "DATA_EMISSAO"),
                (114, 122, "VALOR"),
                (137, 156, "DESTINATARIO"),
                (159, 197, "ENDERECO_DESTINATARIO")
            ]
        }
    ),
    (
        "NF-e Nº. 000.005.377 Série 010 DATA DE RECEBIMENTO IDENTIFICAÇÃO E ASSINATURA DO RECEBEDOR", 
        {
            "entities": [
                (5, 21, "NUMERO_NFE"),
                (28, 31, "SERIE")
            ]
        }
    ),
    (
        "CHAVE DE ACESSO 2525 0506 3528 9300 4299 5501 0000 0053 7719 8482 5896", 
        {
            "entities": [
                (16, 60, "CHAVE_ACESSO")
            ]
        }
    ),
    (
        "NATUREZA DA OPERAÇÃO VENDA MERC.SUJEITA A ST", 
        {
            "entities": [
                (22, 43, "NATUREZA_OPERACAO")
            ]
        }
    ),
    (
        "CNPJ / CPF 06.352.893/0042-99", 
        {
            "entities": [
                (10, 29, "CNPJ_EMITENTE")
            ]
        }
    ),
    (
        "DESTINATÁRIO / REMETENTE NOME / RAZÃO SOCIAL VALTER MARQUES SANTOS CNPJ / CPF 635.896.458-18", 
        {
            "entities": [
                (31, 50, "DESTINATARIO"),
                (63, 77, "CPF_DESTINATARIO")
            ]
        }
    ),
    (
        "DATA DA EMISSÃO 17/05/2024", 
        {
            "entities": [
                (15, 25, "DATA_EMISSAO")
            ]
        }
    ),
    (
        "VALOR TOTAL DA NOTA 630,56", 
        {
            "entities": [
                (20, 26, "VALOR_TOTAL")
            ]
        }
    ),

    (
        "RECEBEMOS DE REDMIL ELETRONICOS S.A. OS PRODUTOS E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL ELETRÔNICA INDICADA ABAIXO. EMISSÃO: 11/05/2023 VALOR TOTAL: R$ 925,27 DESTINATÁRIO: JONATHAS AMORIM - RUA PIAUI, 32 - LAGOINHA BRASILIA-DF",
        {"entities": [
            (12, 35, "EMITENTE"),
            (87, 97, "DATA_EMISSAO"),
            (111, 119, "VALOR_TOTAL"),
            (133, 148, "DESTINATARIO"),
            (151, 178, "ENDERECO_DEST")
        ]}
    ),
    (
        "NF-e Nº. 000.982.124 Série 006",
        {"entities": [
            (6, 18, "NUMERO_NF"),
            (26, 29, "SERIE")
        ]}
    ),
    (
        "CHAVE DE ACESSO 9935 2515 6161 7000 0224 5500 6000 9821 2415 4386 5552",
        {"entities": [
            (16, 59, "CHAVE_ACESSO")
        ]}
    ),
    (
        "PROTOCOLO DE AUTORIZAÇÃO DE USO 323420103745834 - 11/05/2023 09:57:08",
        {"entities": [
            (34, 49, "PROTOCOLO_AUT"),
            (52, 62, "DATA_AUTORIZACAO"),
            (63, 71, "HORA_AUTORIZACAO")
        ]}
    ),
    (
        "CNPJ / CPF 03.106.170/0002-24",
        {"entities": [
            (10, 27, "CNPJ_EMITENTE")
        ]}
    ),
    (
        "DESTINATÁRIO / REMETENTE NOME / RAZÃO SOCIAL JONATHAS AMORIM CNPJ / CPF 874.365.258-69",
        {"entities": [
            (55, 70, "CPF_DEST")
        ]}
    ),
    (
        "DATA DA EMISSÃO 11/05/2023",
        {"entities": [
            (17, 27, "DATA_EMISSAO")
        ]}
    ),
    (
        "FATURA / DUPLICATA Num. 001 Venc. 10/07/2023 Valor R$ 925,27",
        {"entities": [
            (31, 41, "DATA_VENCIMENTO"),
            (48, 56, "VALOR_TOTAL")
        ]}
    ),
    (
        "TRANSPORTADOR / VOLUMES TRANSPORTADOS NOME / RAZÃO SOCIAL BRASPRESS TRANSPORTES URGENTES LTDA CNPJ / CPF 48.740.351/0127-67",
        {"entities": [
            (44, 78, "TRANSPORTADORA"),
            (88, 106, "CNPJ_TRANSPORTADORA")
        ]}
    ),
    (
        "PESO BRUTO 3,460 PESO LÍQUIDO 2,870",
        {"entities": [
            (11, 16, "PESO_BRUTO"),
            (30, 35, "PESO_LIQUIDO")
        ]}
    ),
    (
        "BLSTAG9630-011 CARREGADOR CELULAR REDMIL vICMSUFDest=9,21",
        {"entities": [
            (0, 13, "COD_PRODUTO"),
            (14, 42, "DESCRICAO_PRODUTO"),
            (55, 59, "ICMS_DEST")
        ]}
    ),
    (
        "BLSTMG-BR8-357 CABO USB-C vICMSUFDest=24,49",
        {"entities": [
            (0, 13, "COD_PRODUTO"),
            (14, 24, "DESCRICAO_PRODUTO"),
            (36, 41, "ICMS_DEST")
        ]}
    )
    
]


# Define o componente NER no pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")
ner.add_label("PAGADOR")
ner.add_label("CPF")

# Desabilita outras partes do pipeline para acelerar o treinamento
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  
    # Configura o treinamento
    optimizer = nlp.begin_training()
    for i in range(30):  # 30 épocas
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Perda na época {i}: {losses}")

# Salva o modelo ajustado
output_dir = "./ner_model"
nlp.to_disk(output_dir)
print("Modelo salvo em:", output_dir)
