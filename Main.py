from UserLogin import *
from SubredditTracker import *



def main():
    CLIENT_ID = ""
    SECRET_TOKEN = ""
    username = ""
    password = ""

    user_login = UserLogin()
    user_login.run()

    subreddit_tracker = SubredditTracker(CLIENT_ID, SECRET_TOKEN, username, password)
    subreddit_tracker.track()


if __name__ == "__main__":
    main()