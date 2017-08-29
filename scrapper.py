import tweepy
from tweepy import OAuthHandler
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
from Logger.strategies import NormalLogStrategy
from persistance.datasetPersistance import DatasetPersistance
from utils.ostruct import *

TRACK_TERMS = ["python", "la caja", "alberdi"]
CONNECTION_STRING = "sqlite:///mydatabase.db'"
CSV_NAME = "tweets.csv"
TABLE_NAME = "scrapping"

logger = NormalLogStrategy('TweetpyLogger')

with open('credentials.json') as data_file:
    credentials = json.load(data_file)

logger.info('Starting tweet streaming')

tweet_database = DatasetPersistance("sqlite:///myDownloadTweets.db", "tweets")


def persist_tweet(table, data):
    try:
        table.insert(dict(
            user_description=data.description,
            user_location=data.loc,
            coordinates=data.coords,
            text=data.text,
            geo=data.geo,
            user_name=data.name,
            user_created=data.user_created,
            user_followers=data.followers,
            id_str=data.id_str,
            created=data.created,
            retweet_count=data.retweets,
            user_bg_color=data.bg_color,
            polarity=data.polarity,
            subjectivity=data.subjectivity,
        ))
    except ProgrammingError as err:
        print(err)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.retweeted:
            return

        coords = status.coordinates
        text = status.text
        geo = status.geo

        tweet = OpenStruct()
        tweet.description = status.user.description
        tweet.loc = status.user.location
        tweet.text = status.text
        tweet.coords = coords
        tweet.geo = geo
        tweet.name = status.user.screen_name
        tweet.user_created = status.user.created_at
        tweet.followers = status.user.followers_count
        tweet.id_str = status.id_str
        tweet.created = status.created_at
        tweet.retweets = status.retweet_count
        tweet.bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        tweet.blob = blob

        sent = blob.sentiment

        tweet.polarity = sent.polarity
        tweet.subjectivity = sent.subjectivity

        logger.info("got tweet from user {0} with text: {1}".format(status.user.screen_name, text))

        if geo is not None:
            tweet.geo = json.dumps(geo)

        if coords is not None:
            logger.info("Found tweet with geo coordinates!!")
            tweet.coords = json.dumps(coords)

        tweet_database.persist_to_table("tweets", tweet, persist_tweet)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=TRACK_TERMS)
