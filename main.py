import pandas as pd
import datetime
from datetime import datetime as dt
from credenciales import redditauth
from kinou import nube_palabras, freq_palabras
from pathlib import Path

reddit = redditauth()

# Toma la fecha actual para el estampado en cada archivo posterior. 👇
filename_date = dt.now().strftime('%Y-%m-%d')  # -%H-%M removido del filename

# Armo un diccionario con los 10 posts más populares del subreddit "Argentina".
post_dict = {"id": [],
             "context": [],
             "text": [],
             "upv": [],
             "author": [],
             "date": [],
             "type": [],
             }
arg_subreddit = reddit.subreddit('Argentina')
for post in arg_subreddit.top(limit=10, time_filter='day'):
    post_dict["id"].append(post.id)
    post_dict["context"].append(post.id)
    post_dict["text"].append(post.title)
    post_dict["upv"].append(post.score)
    post_dict["author"].append(post.author)
    post_dict["date"].append(filename_date)
    post_dict['type'].append('post')

# Se convierte el diccionario en un data frame.
temas = pd.DataFrame(post_dict)
# Se convierte el dataframe en un CSV para posterior análisis. (comentar cuando se hagan pruebas)
temas.to_csv(f"{Path.cwd()}/Bases/Reddit_Arg_Temas{filename_date}.csv")
dataset = pd.read_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv", index_col=0)
nuevods = pd.concat([dataset, temas], sort=False)
nuevods.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")

# Mismo procedimiento anterior pero para los comentarios de cada post.
lista_ids = temas["id"]
for postid in lista_ids:
    comment_dict = {"id": [],
                    "context": [],
                    "text": [],
                    "upv": [],
                    "author": [],
                    "date": [],
                    "type": [],
                    }
    posteo = reddit.submission(postid)
    posteo.comments.replace_more(limit=0)
    for comentario in posteo.comments.list():
        if comentario.author == 'empleadoEstatalBot':  # Elimina el bot que postea la noticia en caso de existir.
            continue
        comment_dict["id"].append(comentario.id)
        p_split = comentario.parent_id.split('_')
        idctx = p_split[1]
        comment_dict['context'].append(idctx)
        comment_dict["text"].append(comentario.body)
        comment_dict["upv"].append(comentario.score)
        comment_dict["author"].append(comentario.author)
        comment_dict['date'].append(filename_date)
        comment_dict['type'].append('comment')
    dataset = pd.read_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv", index_col=0)
    comms = pd.DataFrame(comment_dict)
    nuevods = pd.concat([dataset, comms], sort=False)
    nuevods.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Dataset.csv")
    comms.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Comm_Post-{postid}-{filename_date}.csv")
    archivo = f"Red_Arg_Comm_Post-{postid}-{filename_date}.csv"
    nube_palabras(archivo)
    freq_palabras(archivo)
