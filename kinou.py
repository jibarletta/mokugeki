import pandas as pd
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator # No se usa, remover.
from wordcloud import STOPWORDS           # No se usa, remover.
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# Primero cargamos las stop words a ser utilizadas en cada una de las funciones presentes.

nltk.download("stopwords")
stopwords = set(stopwords.words("spanish"))
stopwords.update(["que", "de", "el", "por", "se", "está", "lo", "en", "si", "https", "preview", "redd", "it", "qu",
                  "giphy", "gif", "jpeg", "webp", "www", "png"])


# Definimos la función que vamos a utilizar para el armado de la wordcloud.
def nube_palabras(archivo):
    """Toma el post y crea la nube de palabras."""
    file = pd.read_csv(f"Bases/{archivo}")
    data = ','.join(file["comentario"])
    data = data.lower()
    # print(len(data))  # TODO: No sirven mas, eliminar.
    # print(data)       # TODO: No sirven mas, eliminar.
    wordcloud = WordCloud(stopwords=stopwords).generate(data)
    wordcloud.to_file(f"Bases/{archivo}.png")
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()  # TODO: Guardar imagen en carpeta con mismo formato de los otros archivos.


# Definimos la función para obtener una tabla de frecuencias de palabras.

def freq_palabras(archivo):
    """Toma el post y crea la tabla de frecuencias de palabras."""
    file = pd.read_csv(f"Bases/{archivo}")
    tabla_dict = {"palabra": [], "frecuencia": []}
    data = ','.join(file["comentario"])
    data.lower()
    conteo = WordCloud(stopwords=stopwords).process_text(data)
    for word in conteo:
        tabla_dict["palabra"].append(word)
        tabla_dict["frecuencia"].append(conteo[word])
    tabla = pd.DataFrame(tabla_dict)
    tabla = tabla.sort_values(by="frecuencia", ascending=False)
    tabla.to_csv(f"Bases/{archivo}-TC.csv")   # TODO: usar mismo formato de archivos y guardar en carpeta. ojo el .csv final aca
    return tabla    # Este return se agregó para las pruebas. Revisar.

# TODO: Borrar el código inferior, quedó para pruebas.
# archivo = "Red_Arg_Comm_Post-1dji1nx--2024-06-19-19-11.csv"
#
# nube_palabras(archivo)
# print(freq_palabras(archivo))
