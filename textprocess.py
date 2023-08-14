import spacy
#python -m spacy download es_core_news_sm   para descargar el modelo en español

def getPerson(text):
    spanish_nlp = spacy.load('es_core_news_sm')

    # text = open('texto.txt', 'r', encoding="UTF-8").read()
    text = text.replace('“', '')

    spacy_parser = spanish_nlp(text)

    lista = list()

    for entity in spacy_parser.ents:
        # print(f'Found: {entity.text} of type: {entity.label_}')
        if entity.label_ == "PER" or entity.label_ == "LOC" or entity.label_ == "ORG":
           # print("Persona encontrada!!", entity.label_, entity.text)
            lista.append(f'{entity.label_}:{entity.text}')

    return lista



