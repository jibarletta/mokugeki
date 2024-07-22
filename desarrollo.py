import praw
from datetime import datetime as dt
import os
import pandas as pd
from wordcloud import WordCloud as wcloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from pathlib import Path
from credenciales import redditauth

# reddit = redditauth()
# prueba = reddit.submission("1dleo3c")
# print(prueba.title)
#
# archivo = "Reddit_Arg_Temas-2024-06-02-15-38.csv"
#
# #file = pd.read_csv(f"{Path.cwd()}/Bases/{archivo}")
# # f"{Path.cwd()}/Bases/Reddit_Arg_Temas{filename_date}.csv"
#
# archivo = archivo.replace('.csv', "")
# archivo = archivo.split("-")
#
# print(archivo[1])
# print(archivo[2])
# print(archivo[3])
#

dataset_dict = {"idctx": [],
                "contexto": [],
                "upvctx": [],
                "idcom": [],
                "comentario": [],
                "upvcom": []    # Acá se pueden agregar las nuevas categorías que hay que pensar.
                }

for file in os.listdir(f"{Path.cwd()}/Bases/Temas/"):
    file_nlist = file.split('-')
    fecha_file = f"{file_nlist[-3]}-{file_nlist[-2]}-{file_nlist[-1]}"
    df_temp = pd.read_csv(f"{Path.cwd()}/Bases/Temas/{file}", index_col=0)
    for lab, row in df_temp.iterrows():
        dataset_dict['idctx'].append(row['id'])
        dataset_dict['idcom'].append(row['id'])
        dataset_dict['contexto'].append(row['titulo'])
        dataset_dict['comentario'].append(row['titulo'])
        dataset_dict['upvctx'].append(row['upvotes'])
        dataset_dict['upvcom'].append(row['upvotes'])
        df2_temp = pd.read_csv(f"{Path.cwd()}/Bases/Comentarios/Red_Arg_Comm_Post-{row['id']}--{fecha_file}", index_col=0)
        for lab2, row2 in df2_temp.iterrows():
            dataset_dict['idcom'].append(row2['id'])
            dataset_dict['comentario'].append(row2['comentario'])
            dataset_dict['upvcom'].append(row2['upvotes'])
            p_split = row2['parent'].split('_')
            dataset_dict['contexto'].append(f"{p_split[1]}")
dataset = pd.DataFrame.from_dict(dataset_dict, orient='index')
dataset = dataset.transpose()
dataset.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")
    # print(file)

# Red_Arg_Comm_Post-1e5866w--2024-07-17.csv
