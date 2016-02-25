#Variables that contains the user credentials to access Twitter API
config = {
    "access_key": "489012752-9FZjNu4JzHyB5k4cilD9KfstmfGA3DTNzfHT9mMf",
    "access_secret": "4eoIqxiNX1j39pWzeOalq1MGIbDc4iBTh4AwJl48ZsWQL",
    "consumer_key": "UHs7stMzmywU93SThCHw5oKa0",
    "consumer_secret": "KIlpeXHihwwMvXfNId7hZbmAOzqBTbk2wrc6EpVZIw9hNYzI6E"
}

import base64
import datetime
import json
import pytz
import requests
import urllib
from dateutil import parser
from pprint import pprint

user_id = 489012752
user_name = "RaajSupramanian"

base_path = "https://api.twitter.com/"
followers_url = base_path + "1.1/followers/ids.json"
tweets_url = base_path + "1.1/statuses/user_timeline.json"
url_params = "?screen_name=RaajSupramanian&user_id=489012752"
today = datetime.datetime.now(pytz.utc)
last_week_date = today - datetime.timedelta(days=7)



def _get_response(resp_obj):
    #print resp_obj.status_code
    if resp_obj.status_code == 200:
        response_data = json.loads(resp_obj.content)
        #print response_data
        return response_data
    #print "Error in response"
    print resp_obj.content
    return None

def _get_bearer_token():
    encoded_CONSUMER_KEY = urllib.quote(config['consumer_key'])
    encoded_CONSUMER_SECRET = urllib.quote(config['consumer_secret'])
    concat_consumer_url = encoded_CONSUMER_KEY + ":" + encoded_CONSUMER_SECRET
    token_url = '/oauth2/token/'
    url = base_path + token_url
    payload = {'grant_type' : 'client_credentials'}
    headers = {"User-Agent": "My Twitter 1.1",
               "Authorization": "Basic %s" % base64.b64encode(concat_consumer_url),
               "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
               "Accept-Encoding": "gzip"}
    resp = requests.post(url, data=payload, headers=headers)
    return _get_response(resp)

def _get_headers():
    bearer_resp = _get_bearer_token()
    headers = {"Authorization" : bearer_resp["token_type"] +" "+ bearer_resp["access_token"],
               "Accept-Encoding": "gzip",
               "User-Agent": "My Twitter 1.1"}
    return headers

def get_followers_ids():
    params = {"screen_name": user_name, "user_id": user_id}
    followers_resp = requests.get(followers_url, params=params, headers=_get_headers())
    return _get_response(followers_resp)["ids"]

def per_follower_tweet_details(follower_id):
    params = {"user_id": follower_id}
    follower_response = requests.get(tweets_url, params=params, headers=_get_headers())
    follower_details = _get_response(follower_response)
    date_counts = []
    if follower_details:
        for detail in follower_details:
            tweet_date = parser.parse(detail["created_at"])
            dates = []
            if last_week_date < tweet_date < today:
                if tweet_date not in dates:
                    date_counts.append({tweet_date : 1})
                    dates.append(tweet_date)
                else:
                    for t_d in date_counts:
                        if tweet_date in t_d.keys():
                            present_val = t_d[tweet_date]
                            date_counts.remove(t_d)
                            date_counts.append({tweet_date: present_val+1})
    return date_counts

def get_tweet_details():
    tweet_detail_dict = {}
    folower_ids = get_followers_ids()
    for folower_id in folower_ids:
        tweet_detail_dict[folower_id] = per_follower_tweet_details(folower_id)
    pprint(tweet_detail_dict)

get_tweet_details()