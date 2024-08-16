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
    df_temas = pd.read_csv(f"{Path.cwd()}/Bases/Temas/{file}", index_col=0)
    file_nlist = file.split('-')
    fecha_file = f"{file_nlist[-3]}-{file_nlist[-2]}-{file_nlist[-1]}"
    for lab, row in df_temas.iterrows():
        dataset_dict['id'].append(row['id'])
        dataset_dict['context'].append(row['id'])
        dataset_dict['text'].append(row['titulo'])
        dataset_dict['upv'].append(row['upvotes'])
        dataset_dict['author'].append(row['autor'])
        dataset_dict['date'].append(fecha_file[0:10])
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

# dataset = pd.read_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv", index_col=0)
dataset2 = pd.DataFrame.from_dict(dataset_dict)
# nuevods = pd.concat([dataset, dataset2], sort=False)
dataset2.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")
