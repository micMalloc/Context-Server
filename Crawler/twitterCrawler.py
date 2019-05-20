import oauth2
import datetime
import json
from Handler import twitterHandler


class TwitterCrawler:

    def __init__(self):
        self.CONSUMER_KEY = "TxRrlOz7Djdj3h4NEk6guG2jA"
        self.CONSUMER_SECRET = "sAFUdHMn1G9zaCbfbOjEdVYdxRoj7PQoIY7VzwLuaQxYM6tldM"
        self.ACCESS_TOKEN = "2163239922-ZtH10FjhhP5VcesaukPIIjD8RiRpjHXmKkbK6uK"
        self.ACCESS_SECRET = "ct7cKaE7xV5PAmb7cYrTgNJ11rLEarzBm0yyHgI95hS26"
        self.handler = twitterHandler.TwitterHandler()

    def oauth2_request(self, consumer_key, consumer_secret, access_token, access_secret):
        try:
            consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
            token = oauth2.Token(key=access_token, secret=access_secret)
            client = oauth2.Client(consumer, token)
            return client
        except Exception as e:
            print(e)
            return None

    def get_user_timeline(self, client, screen_name, count=200, include_rts='False'):
        base = "https://api.twitter.com/1.1"
        node = "/statuses/user_timeline.json"
        fields = "?screen_name=%s&count=%s&include_rts=%s" % (screen_name, count, include_rts)
        # fields = "?screen_name=%s" % (screen_name)
        url = base + node + fields

        response, data = client.request(url)

        try:
            if response['status'] == '200':
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(e)
            return None

    def get_twitter_tweet(self, tweet, jsonResult):
        tweet_id = tweet['id_str']
        tweet_message = '' if 'text' not in tweet.keys() else tweet['text']

        screen_name = '' if 'user' not in tweet.keys() else tweet['user']['screen_name']

        tweet_link = ''
        if tweet['entities']['urls']:  # list
            for i, val in enumerate(tweet['entities']['urls']):
                tweet_link = tweet_link + tweet['entities']['urls'][i]['url'] + ' '
        else:
            tweet_link = ''

        hashtags = ''
        if tweet['entities']['hashtags']:  # list
            for i, val in enumerate(tweet['entities']['hashtags']):
                hashtags = hashtags + tweet['entities']['hashtags'][i]['text'] + ' '
        else:
            hashtags = ''

        if 'created_at' in tweet.keys():
            # Twitter used UTC Format. EST = UTC + 9(Korean Time) Format ex: Fri Feb 10 03:57:27 +0000 2017
            tweet_published = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            tweet_published = tweet_published + datetime.timedelta(hours=+9)
            tweet_published = tweet_published.strftime('%Y-%m-%d %H:%M:%S')
        else:
            tweet_published = ''

        num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
        num_comments = 0
        num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
        num_likes = num_favorite_count
        num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

        jsonResult.append({'post_id': tweet_id, 'message': tweet_message,
                       'name': screen_name, 'link': tweet_link,
                       'created_time': tweet_published, 'num_reactions': num_favorite_count,
                       'num_comments': num_comments, 'num_shares': num_shares,
                       'num_likes': num_likes, 'num_loves': num_loves,
                       'num_wows': num_wows, 'num_hahas': num_hahas,
                       'num_sads': num_sads, 'num_angrys': num_angrys, 'hashtags': hashtags})

    def run(self):
        screen_name = "seoultopis"

        jsonResult = []

        client = self.oauth2_request(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN, self.ACCESS_SECRET)
        tweets = self.get_user_timeline(client, screen_name)

        for tweet in tweets:
            self.get_twitter_tweet(tweet, jsonResult)

        self.handler.extract_promising_data(jsonResult)

        with open('%s_twitter.json' % (screen_name), 'w', encoding='utf8') as outfile:
            str_ = json.dumps(jsonResult,
                            indent=4, sort_keys=True,
                            ensure_ascii=False)
            outfile.write(str_)

        print('%s_twitter.json SAVED' % (screen_name))
