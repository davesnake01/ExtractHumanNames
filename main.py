from elasticsearch import Elasticsearch #Es importante usar la version de elasticsearch 6.4.0
from elasticsearch.helpers import scan
import pandas as pd
from textprocess import getPerson



#Revisar el requirements.txt
#============================


es = Elasticsearch(host='192.168.2.24', port=9200)

def get_data_from_elastic():

    query = {
        "size": 10,
        "query": {
            "bool": {
                "filter": [
                    {
                        "terms": {
                            "codigos": [2433]
                        }
                    }

                ]
            }
        }
}


    rel = scan(client=es,
               query=query,
               size=10, #No tiene ningún efecto, por lo que la limitacion lo da la fecha
               scroll='1m',
               index='clips2023',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True
               )

    # Keep response in a list.
    result = list(rel)

    temp = []

    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])

    # Create a dataframe.
    df = pd.DataFrame(temp)

    return df


def getData():

    df = get_data_from_elastic()

    if df.empty == True:
        print("No hay datos a procesar")

    else:

        print(df.head())
        print(df.columns)
        print(df.size)
        lista = df[
            ['id_noticia','titular', 'texto','pagina', 'fecha_lectura' ]]

        texto = lista['texto']

        #lista.to_excel("2016-2.xlsx")

        for index, row in lista.iterrows():
            # variables
            idnoticia = row["id_noticia"]
            titular = row["titular"]
            texto = getPerson(row["texto"])
            print(idnoticia,titular, texto)


if __name__ == '__main__':
    getData()