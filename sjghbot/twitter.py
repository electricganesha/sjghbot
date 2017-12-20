"""
Tiny wrapper on top of python-wrapper to provide an authtenticated
Twitter API client.
"""
import twitter

from sjghbot import settings


client = twitter.Api(
    consumer_key=settings.TWITTER_CONSUMER_KEY,
    consumer_secret=settings.TWITTER_CONSUMER_SECRET,
    access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
    access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
)
