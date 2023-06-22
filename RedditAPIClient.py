import requests
from datetime import datetime, timedelta

class RedditAPIClient:
    def __init__(self, client_id, secret_token, username, password):
        self.client_id = client_id
        self.secret_token = secret_token
        self.username = username
        self.password = password
        self.headers = {'User-Agent': 'MyBot/0.0.1'}
        self.token = None

    def authenticate(self):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_token)
        data = { 
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.headers)
        self.token = res.json()['access_token']
        self.headers = {**self.headers, **{'Authorization': f"bearer {self.token}"}}


    def get_datetime_filtered_subreddit_posts(self, start_time, end_time):
        if self.token == None:
            self.authenticate()

        res = requests.get("https://oauth.reddit.com/subreddits/new", headers=self.headers)
        filtered_posts = []
        for subreddit in res.json()['data']['children']:
            creation_time = datetime.utcfromtimestamp(subreddit['data']['created_utc'])
            if start_time <= creation_time <= end_time:
                subreddit_name = subreddit['data']['display_name']
                subreddit_id = subreddit['data']['id']
                subreddit_url = f"https://oauth.reddit.com/r/{subreddit_name}/hot"
                posts_res = requests.get(subreddit_url, headers=self.headers)
                for post in posts_res.json()['data']['children']:
                    title = post['data']['title']
                    text = post['data']['selftext']
                    upvotes = post['data']['ups']
                    filtered_posts.append({'id': subreddit_id, 'title': title, 'text': text, 'upvotes': upvotes})
        return filtered_posts
    
