import praw
import pandas as pd
import datetime

reddit = praw.Reddit(client_id='Z-KrV-M1oNEIVQ', 
                     client_secret='7K6-UeRRhCEhoZoaAsLqvTWY92_OPA', 
                     user_agent='mokugeki')

arg_subreddit = reddit.subreddit('Argentina')

# No se qué hace esto todavía
# big_bang = subreddit.created
# big_bang

# Creamos diccionarios correspondientes

topics_dict = {"title": [], "score": [], "id": [], "url": [], "comms_num": [], "created": [], "body": []}
comms_dict = {"topic": [], "score": [], "body": [], "comm_id": [], "created": [], "parent": []}

for post in arg_subreddit.top(limit=10, time_filter='day'):
    topics_dict["title"].append(post.title)
    topics_dict["score"].append(post.score)
    topics_dict["id"].append(post.id)
    topics_dict["url"].append(post.url)
    topics_dict["comms_num"].append(post.num_comments)
    topics_dict["created"].append(post.created)
    topics_dict["body"].append(post.selftext)

len(topics_dict["title"])

topics_data = pd.DataFrame(topics_dict)


def get_date(comment):
    time = comment
    return datetime.datetime.fromtimestamp(time)


timestamps = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp=timestamps)
topics_data.info()

iteration = 1
for topic in topics_data["id"]:
    print(str(iteration))
    iteration += 1
    post = reddit.comment(id=topic)
    for comm in post.comments:
        comms_dict["topic"].append(topic)
        comms_dict["score"].append(comm.score)
        comms_dict["body"].append(comm.body)
        comms_dict["comm_id"].append(comm)
        comms_dict["created"].append(comm.created)
        comms_dict["parent"].append(comm.parent_id)

print("done")

comms_data = pd.DataFrame(comms_dict)

timestamps = comms_data["created"].apply(get_date)

comms_data = comms_data.assign(timestamp=timestamps)


topics_data.to_csv("subreddit_Arg_topics.csv")
comms_data.to_csv("subreddit_Arg_comments.csv")

