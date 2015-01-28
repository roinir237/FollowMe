from datetime import datetime
import re

from celery import Celery
from app.scraper import Scraper
from app.models import Tweet
from app.main import db_session, twitter_api
import random

app = Celery("twitterbot")
app.config_from_envvar('CELERY_CONFIG_MODULE')

@app.task()
def manage_followers():
    friends_ids = twitter_api.GetFriendIDs()
    if len(friends_ids) >= 2000:
        [unfollow.delay(friend_id) for friend_id in random.sample(friends_ids, 200)]
    else:
        follow_based_on_last_tweet.delay()


@app.task()
def follow_based_on_last_tweet():
    tweet = db_session.query(Tweet).filter(Tweet.posted!=None).order_by(Tweet.posted.desc()).first()
    try:
        keyword = re.findall(r'(?<=-)[^\[]*', tweet.title)[0].strip()
        related_tweets = twitter_api.GetSearch(term=keyword, count=100)
        for tweet in related_tweets:
            if tweet.user.followers_count < 600:
                twitter_api.CreateFriendship(user_id=tweet.user.id)
    except:
        pass


@app.task(bind=True, default_retry_delay=30 * 60, max_retries=4)
def unfollow(self, friend_id):
    try:
        twitter_api.DestroyFriendship(user_id=friend_id)
    except:
        self.retry()

@app.task()
def scrape():
    Scraper().fetch_and_persist(db_session)

@app.task()
def post_tweet():
    msg = db_session.query(Tweet).filter_by(posted=None).first()
    if msg is not None:
        try:
            msg.post_to_twitter(twitter_api)
        except: pass
        msg.posted = datetime.now()
        db_session.commit()
    else:
        scrape().delay()

