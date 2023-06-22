import os
import time 
import pandas
from csv import DictWriter
from RedditAPIClient import *


class SubredditTracker:
    def __init__(self, client_id, secret_token, username, password, db_csv_path="./subreddit.csv", refresh_interval_minutes=3 ):
        self.reddit_api_client = RedditAPIClient(client_id, secret_token, username, password)
        self.field_names = ['id', 'title', 'text', 'upvotes']
        self.db_csv_path = db_csv_path
        if not os.path.exists(db_csv_path):
            d = pandas.DataFrame({"id": list(), "title": list(), "text": list(), "upvotes": list()})
            d.to_csv(self.db_csv_path,index=False)

        self.refresh_interval_minutes = refresh_interval_minutes

    def save_to_db(self, subreddit):
        try:
            with open(self.db_csv_path, 'a') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=self.field_names)
                dictwriter_object.writerow(subreddit)
                f_object.close()
        except:
            print('Unable to save subreddit with id', subreddit['id'], ' to db')


    def track(self):
        print('Tracking subreddits...')
        start_time = datetime.utcnow() - timedelta(minutes=self.refresh_interval_minutes)
        end_time = datetime.utcnow() 
        while True:
            sub_reddits = self.reddit_api_client.get_datetime_filtered_subreddit_posts(start_time, end_time)
            for sub_reddit in sub_reddits:
                self.save_to_db(sub_reddit)
                print(f"ID: {sub_reddit['id']}")
                print(f"Title: {sub_reddit['title']}")
                print(f"Text: {sub_reddit['text']}")
                print(f"Upvotes: {sub_reddit['upvotes']}")
                print()
            time.sleep(self.refresh_interval_minutes * 60)
            start_time = datetime.utcnow() - timedelta(minutes=self.refresh_interval_minutes)
            end_time = datetime.utcnow() 



