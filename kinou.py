import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime
import nltk
from nltk.corpus import stopwords
from pathlib import Path


# Primero cargamos las stop words a ser utilizadas en cada una de las funciones presentes.
nltk.download("stopwords")
stopwords = set(stopwords.words("spanish"))
stopwords.update(["que", "de", "el", "por", "se", "está", "lo", "en", "si", "https", "preview", "redd", "it", "qu",
                  "giphy", "gif", "jpeg", "webp", "www", "png", "format", "com", "width"])

# Definimos la función que vamos a utilizar para el armado de la wordcloud.
def nube_palabras(archivo):
    """Toma el post y crea la nube de palabras."""
    file = pd.read_csv(f"{Path.cwd()}/Bases/{archivo}", index_col=0)
    data = ','.join(file["comentario"])
    data = data.lower()
    wordcloud = WordCloud(stopwords=stopwords).generate(data)
    wordcloud.to_file(f"Bases/{archivo}.png")
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


# Definimos la función para obtener una tabla de frecuencias de palabras.
def freq_palabras(archivo):
    """Toma el post y crea la tabla de frecuencias de palabras."""
    file = pd.read_csv(f"{Path.cwd()}/Bases/{archivo}", index_col=0)
    tabla_dict = {"palabra": [], "frecuencia": []}
    data = ','.join(file["comentario"])
    data.lower()
    conteo = WordCloud(stopwords=stopwords).process_text(data)
    for word in conteo:
        tabla_dict["palabra"].append(word)
        tabla_dict["frecuencia"].append(conteo[word])
    tabla = pd.DataFrame(tabla_dict)
    tabla = tabla.sort_values(by="frecuencia", ascending=False)
    tabla.to_csv(f"{Path.cwd()}/Bases/{archivo}-TC.csv")
    return tabla    # Este return se agregó para las pruebas. Revisar.
