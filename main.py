import praw
import pandas as pd
import datetime

reddit = praw.Reddit(client_id='***', client_secret='***', user_agent='mokugeki')

# get 10 hot posts from the Argentina subreddit

post_dict = {"titulo": [], "upvotes": [], "id": [], "comentarios": [], "creado": []}
posts = []
arg_subreddit = reddit.subreddit('Argentina')
for post in arg_subreddit.top(limit=10, time_filter='day'):
    post_dict["titulo"].append(post.title)
    post_dict["upvotes"].append(post.score)
    post_dict["id"].append(post.id)
    post_dict["comentarios"].append(post.num_comments)
    post_dict["creado"].append(datetime.datetime.fromtimestamp(post.created))

temas = pd.DataFrame(post_dict)
print(temas)
temas.to_csv("Reddit_Arg_Temas.csv")

# TODO: Hasta acá perfecto, ahora hay que hacer lo mismo pero para los comentarios.
# TODO: No te olvides de sacar los arboles de comentarios. Es muy importante.
