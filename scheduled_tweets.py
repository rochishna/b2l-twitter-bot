import tweepy
import schedule
import time
from time import sleep
from credentials import *
import sqlite3
import random

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
greet=['hello there','greetings','hey',"'ello there mate"]
project=["How's the project coming","How're the things with your project"]
def run_tasks():
    conn = sqlite3.connect(r'db.sqlite')
    p= conn.execute("select title from users")
    p=list(p)
    conn.close()
    users=[]
    for i in range (len(p)):
        users.append(p[i][0])
#TODO: Add more phrases to the greet and project list
    for user in users:
        tweet = greet[random.randrange(len(greet))]+" "+"@"+user+" "+project[random.randrange(len(project))]
        api.update_status(status=tweet)
# TODO: change it to one a week#DONE
    schedule.every(10080).minutes.do(run_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)
    return
# TODO: Add emojis / images / gifs to the responses

if __name__ == "__main__":
    run_tasks()