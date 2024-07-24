import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from pathlib import Path
import os
import shutil


# Definimos la función que vamos a utilizar para el armado de la wordcloud.
def nube_palabras(archivo):
    # Primero cargamos las stop words a ser utilizadas en cada una de las funciones presentes.
    nltk.download("stopwords")
    stopwords = set(stopwords.words("spanish"))
    stopwords.update(["que", "de", "el", "por", "se", "está", "lo", "en", "si", "https", "preview", "redd", "it", "qu",
                      "giphy", "gif", "jpeg", "webp", "www", "png", "format", "com", "width"])
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
    # Primero cargamos las stop words a ser utilizadas en cada una de las funciones presentes.
    nltk.download("stopwords")
    stopwords = set(stopwords.words("spanish"))
    stopwords.update(["que", "de", "el", "por", "se", "está", "lo", "en", "si", "https", "preview", "redd", "it", "qu",
                      "giphy", "gif", "jpeg", "webp", "www", "png", "format", "com", "width"])
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

# TODO: Proba armar el diccionario antes, hacerlo un DF y luego concatenarlo.

# Defino la función para agregar al dataset los temas del día.
def ds_add_temas(diccionario):
    dataset_dict = {"id": [],
                    "context": [],
                    "text": [],
                    "upv": [],
                    "author": [],
                    "date": [],
                    "type": [],
                    }
    dataset = pd.read_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv", index_col=0)
    # file = pd.read_csv(f"{Path.cwd()}/Bases/Temas/{temas}", index_col=0)
    df_temp = pd.read_csv(f"{Path.cwd()}/Bases/Temas/{temas}", index_col=0)
    df_temas = df_temp[1:6]
    df_temas.set_index('id')
    for lab, row in df_temas.iterrows():
        dataset_dict['id'].append(row['id'])
        dataset_dict['context'].append(row['id'])
        dataset_dict['text'].append(row['titulo'])
        dataset_dict['upv'].append(row['upvotes'])
        dataset_dict['author'].append(row['autor'])
        fecha_post = row['creado'].split(' ')
        fecha_post = fecha_post[0]
        dataset_dict['date'].append(fecha_post)
        dataset_dict['type'].append('post')
    shutil.move(f"{Path.cwd()}/Bases/Temas/{temas}", f"{Path.cwd()}/Bases/Procesados/Temas")
    ds_temas = pd.DataFrame(dataset_dict)
    nuevods = pd.concat([dataset, ds_temas])
    nuevods.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")

# Defino la función para agregar los comentarios al data set.
def ds_add_coms(dataset_p, diccionario):
    comment_dict = {"id": [],
                    "comentario": [],
                    "upvotes": [],
                    "parent": [],
                    "autor": []
                    }
    dfcoms = pd.DataFrame(comentarios)
    dataset = pd.read_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv", index_col=0)
    file_nlist = comentarios.split('-')
    fecha_file = f"{file_nlist[-3]}-{file_nlist[-2]}-{file_nlist[-1]}"
    df2_temp = pd.read_csv(f"{Path.cwd()}/Bases/Comentarios/{comentarios}", index_col=0)
    # for lab2, row2 in df2_temp.iterrows():
    for lab2, row2 in df2_temp.iterrows():
        if row2["autor"] == 'empleadoEstatalBot':  # Elimina el bot que postea la noticia en caso de existir.
            continue
        comment_dict['id'].append(row2['id'])
        p_split = row2['parent'].split('_')
        idctx = p_split[1]
        comment_dict['context'].append(idctx)
        comment_dict['text'].append(row2['comentario'])
        comment_dict['upv'].append(row2['upvotes'])
        comment_dict['author'].append(row2['autor'])
        comment_dict['date'].append(fecha_file[0:10])
        comment_dict['type'].append('comment')
    nuevocomds = pd.DataFrame(comment_dict)
    nuevocmds = pd.concat(dataset, nuevocomds)
    # dataset.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")

# TODO: Borrar el código inferior, quedó para pruebas.
# archivo = "Red_Arg_Comm_Post-1dji1nx--2024-06-19-19-11.csv"
#
# nube_palabras(archivo)
# print(freq_palabras(archivo))

temas = 'Reddit_Arg_Temas-2024-07-21.csv'
comentarios = 'Red_Arg_Comm_Post-1e8jkcj--2024-07-21.csv'

ds_add_temas(temas)
ds_add_coms(comentarios)
