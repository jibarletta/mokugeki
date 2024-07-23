import os
import pandas as pd
from pathlib import Path

dataset_dict = {"id": [],
                "context": [],
                "text": [],
                "upv": [],
                "author": [],
                "date": [],
                "type": [],
                }

for file in os.listdir(f"{Path.cwd()}/Bases/Temas/"):
    df_temp = pd.read_csv(f"{Path.cwd()}/Bases/Temas/{file}")
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

for file in os.listdir(f'{Path.cwd()}/Bases/Comentarios/'):
    file_nlist = file.split('-')
    fecha_file = f"{file_nlist[-3]}-{file_nlist[-2]}-{file_nlist[-1]}"
    df2_temp = pd.read_csv(f"{Path.cwd()}/Bases/Comentarios/{file}", index_col=0)
    for lab2, row2 in df2_temp.iterrows():
        if row2["autor"] == 'empleadoEstatalBot':    # Elimina el bot que postea la noticia en caso de existir.
            continue
        dataset_dict['id'].append(row2['id'])
        p_split = row2['parent'].split('_')
        idctx = p_split[1]
        dataset_dict['context'].append(idctx)
        dataset_dict['text'].append(row2['comentario'])
        dataset_dict['upv'].append(row2['upvotes'])
        dataset_dict['author'].append(row2['autor'])
        dataset_dict['date'].append(fecha_file[0:10])
        dataset_dict['type'].append('comment')

dataset = pd.DataFrame.from_dict(dataset_dict)
dataset.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")
