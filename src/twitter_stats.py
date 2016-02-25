import base64
import json
import requests
import urllib
from constants import *
from dateutil import parser


class TweetCount(object):
    def __init__(self):
        """
        Init method to initialize common variables
        """
        self.headers = self._get_headers() # initiated here which will save repeated call for headers
        self.followers_count = 0
        self.not_authorized_followers = 0
        self.total_tweets = 0
        self.total_tweets_per_follower = []

    def _get_response(self, resp_obj):
        """
        Common Method to look up on response object.
        Also count # 401s
        :param resp_obj: needs response object to process
        :return: dict of response if success else None
        """
        if resp_obj.status_code == 200:
            response_data = json.loads(resp_obj.content)
            return response_data
        elif resp_obj.status_code == 401:
            self.not_authorized_followers += 1 # increments unauthorised users
        return None

    def _get_bearer_token(self):
        """
        private function to get bearer token for authorization
        :return: bearer token value
        """
        # url quote for key and secret
        enc_consumer_key = urllib.quote(config['consumer_key'])
        enc_consumer_secret = urllib.quote(config['consumer_secret'])
        concat_consumer_url = enc_consumer_key + ":" + enc_consumer_secret

        token_url = '/oauth2/token/'
        url = base_path + token_url

        payload = {'grant_type' : 'client_credentials'}

        headers = {"User-Agent": "My Twitter 1.1",
                   "Authorization": "Basic %s" % base64.b64encode(concat_consumer_url),
                   "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                   "Accept-Encoding": "gzip"}

        resp = requests.post(url, data=payload, headers=headers)
        return self._get_response(resp)

    def _get_headers(self):
        """
        common function where header details are initialized in init for requests
        :return: header dict
        """
        bearer_resp = self._get_bearer_token()

        headers = {"Authorization" : bearer_resp["token_type"] + " " + bearer_resp["access_token"],
                   "Accept-Encoding": "gzip",
                   "User-Agent": "My Twitter 1.1"}
        return headers

    def get_followers_ids(self):
        """
        This function gets all followers id for the authenticated user
        :return: list of followers ids
        """
        params = {"screen_name": user_name, "user_id": user_id}
        followers_resp = requests.get(followers_url, params=params, headers=self.headers)
        return self._get_response(followers_resp)["ids"]

    def per_follower_tweet_details(self,follower_id):
        """
        Gets Tweets data for a particular follower_id
        loops through above response and prepares data for displaying
        :return: Count of tweets for each follower_id on each day
        """
        params = {"user_id": follower_id}

        follower_response = requests.get(tweets_url, params=params, headers=self.headers)
        follower_details = self._get_response(follower_response)

        date_counts = []
        if follower_details: # needs to be checked as there are some secured followersw whose data is unauthorized
            twt_count = 0  # tweet counter
            dates = [] # list of dates

            for detail in follower_details:
                # parse "Thu Feb 25 11:55:16 +0000 2016" to python datetime format for comparison
                tweet_date = parser.parse(detail["created_at"]).date()
                if last_week_date < tweet_date < today:  # check if parsed date is between the range of dates (one week)
                    twt_count += 1  # incrment the counter
                    if tweet_date not in dates:  # check before appending to list of dates
                        date_counts.append({tweet_date : 1})
                        dates.append(tweet_date)
                    else:
                        for t_d in date_counts:  # for incrementing value in dates list if already present
                            if tweet_date in t_d.keys():
                                present_val = t_d[tweet_date]
                                date_counts.remove(t_d)
                                date_counts.append({tweet_date: present_val+1})
            self.total_tweets_per_follower.append({follower_id:twt_count})  # Total tweets per follower for this period
            self.total_tweets += twt_count # Overall total tweets count
        return date_counts

    def get_tweet_details(self):
        """
        Consolidating function to call and summarize all other functions
        """
        tweet_detail_dict = {}
        folower_ids = self.get_followers_ids()
        self.followers_count = len(folower_ids)
        print "Fetching Data Please wait .",
        for folower_id in folower_ids:
            print ".",
            tweet_detail_dict[folower_id] = self.per_follower_tweet_details(folower_id)
        self.furnish_data()  # handle moves to displaying function

    def furnish_data(self):
        """
        Aggregation and display function of all data
        """
        print "\nData Analysis on Followers between %s and %s" % (last_week_date, today)
        print "Total Followers : %s " % self.followers_count
        print "Total Unauthorized Followers (Can't Fetch data) : %s" % self.not_authorized_followers
        print "Total Tweets : %s" % self.total_tweets
        print "Tweets per user ids"
        max_count = 0
        max_tweet = [{"dummy":max_count}]
        for user in self.total_tweets_per_follower:
            print "\t%s : %s" % (user.items()[0])
            if user.items()[0][1] > max_count:
                max_count = user.items()[0][1]
                del max_tweet[:]
                max_tweet.append(user)
            elif user.items()[0][1] == max_count:
                max_tweet.append(user)
        print "Max Tweets details: "
        for usr in max_tweet:
            print "Max Tweet user %s and his count is %s" % (usr.items()[0])


if __name__ == "__main__":
    # make the file runable by just saying "python twitter_stats.py"
    class_obj = TweetCount()
    class_obj.get_tweet_details()
