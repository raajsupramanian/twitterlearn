"""
Constants file for setting up configs
"""

import datetime
import pytz

# Variables that contains the user credentials to access Twitter data
config = {
    "access_key": "489012752-9FZjNu4JzHyB5k4cilD9KfstmfGA3DTNzfHT9mMf",
    "access_secret": "4eoIqxiNX1j39pWzeOalq1MGIbDc4iBTh4AwJl48ZsWQL",
    "consumer_key": "UHs7stMzmywU93SThCHw5oKa0",
    "consumer_secret": "KIlpeXHihwwMvXfNId7hZbmAOzqBTbk2wrc6EpVZIw9hNYzI6E"
}

user_id = 489012752
user_name = "RaajSupramanian"

# Various paths for accessing data
base_path = "https://api.twitter.com/"
followers_url = base_path + "1.1/followers/ids.json"
tweets_url = base_path + "1.1/statuses/user_timeline.json"
url_params = "?screen_name=RaajSupramanian&user_id=489012752"

# datetime constants
today = datetime.datetime.now(pytz.utc).date()
last_week_date = today - datetime.timedelta(days=7)