import os
import pandas as pd

import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re

from textblob import TextBlob

import warnings
warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

consumer_key = 'deJGtAEIsgfrIbkCDnZAWCcvp'
consumer_secret = 'a8Ar7tDVcq0HDTESQ0uAkomqaFgQwUkxzq2TU8xXLyg1JGUEpE'
access_token = '1188982823631446016-s0tiSHemQlSiYJb9T5HWCGEbQNI0E8'
access_token_secret = 'AkKq6I9sfo3gqGRaryqEXDM1GgugR37CCbspuJosmVzgq'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())




def get_tweet_sentiment(self, tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(self.clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def getTweets(fetched_tweets):
    tweets = []
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        #parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)

        # return parsed tweets
    return tweets


search_term = "#iphone+11 OR #apple+11 OR #iphone11 since:2019-09-20"
tweets = tw.Cursor(api.search,
                   q=search_term,lang="en").items(1000)

#tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]
tweets_no_urls = []
for tweet in tweets:
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        tweets_no_urls.append(remove_url(tweet.text))

print(tweets_no_urls)
sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]

sentiment_objects[0].polarity, sentiment_objects[0]

sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

sentiment_values[0]

sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

print(sentiment_df)