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
    # Adicione mais exemplos aqui
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
