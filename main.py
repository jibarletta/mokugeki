import praw
import pandas as pd
import datetime
from datetime import datetime as dt
from credenciales import redditauth
from kinou import nube_palabras, freq_palabras
from pathlib import Path
from os import chdir

reddit = redditauth()

# Toma la fecha actual para el estampado en cada archivo posterior. 👇
filename_date = dt.now().strftime('-%Y-%m-%d')  # -%H-%M removido del filename

# Armo un diccionario con los 10 posts más populares del subreddit "Argentina".
post_dict = {"titulo": [],
             "upvotes": [],
             "id": [],
             "comentarios": [],
             "creado": [],
             "autor": []
             }
arg_subreddit = reddit.subreddit('Argentina')
for post in arg_subreddit.top(limit=10, time_filter='day'):
    post_dict["titulo"].append(post.title)
    post_dict["upvotes"].append(post.score)
    post_dict["id"].append(post.id)
    post_dict["comentarios"].append(post.num_comments)
    post_dict["creado"].append(datetime.datetime.fromtimestamp(post.created))
    post_dict["autor"].append(post.author)

# Se convierte el diccionario en un data frame.
temas = pd.DataFrame(post_dict)

# Se convierte el dataframe en un CSV para posterior análisis. (comentar cuando se hagan pruebas)
temas.to_csv(f"{Path.cwd()}/Bases/Reddit_Arg_Temas{filename_date}.csv")    # TODO: Guardar en carpetas correspondientes

# Mismo procedimiento anterior pero para los comentarios de cada post.
lista_ids = temas["id"]
for postid in lista_ids:
    comment_dict = {"id": [],
                    "comentario": [],
                    "upvotes": [],
                    "parent": [],
                    "autor": []
                    }
    posteo = reddit.submission(postid)
    posteo.comments.replace_more(limit=0)
    for comentario in posteo.comments.list():
        comment_dict["id"].append(comentario.id)
        comment_dict["comentario"].append(comentario.body)
        comment_dict["upvotes"].append(comentario.score)
        comment_dict["parent"].append(comentario.parent_id)
        comment_dict["autor"].append(comentario.author)
        if comment_dict["autor"][0] == 'empleadoEstatalBot':   # TODO: Probar!!!
            del comment_dict["id"][0]
            del comment_dict["comentario"][0]
            del comment_dict["upvotes"][0]
            del comment_dict["parent"][0]
            del comment_dict["autor"][0]
    comments_del_post = pd.DataFrame(comment_dict)
    comments_del_post.to_csv(f"{Path.cwd()}/Bases/Red_Arg_Comm_Post-{postid}-{filename_date}.csv") # TODO: Guardar en carpetas correspondientes
    archivo = f"Red_Arg_Comm_Post-{postid}-{filename_date}.csv"
    nube_palabras(archivo)
    freq_palabras(archivo)

# TODO: Llamar a las dos funciones para el wordcloud y la tabla de frecuencias.
# TODO: El próximo paso sería realizar el análisis con NLP.
# TODO: Por el lado técnico lo siguiente es armar carpetas y sub carpetas para ubicar los CSV cada día.
# TODO: Siguiente a este proceso es elevar este script en el docker del servidor para su automatización.
