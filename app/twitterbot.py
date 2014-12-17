from datetime import datetime
import re

from celery import Celery
from celery import Task

from app.scraper import Scraper
from app.models import Tweet
from app.main import db_session, twitter_api


app = Celery("twitterbot")
app.config_from_envvar('CELERY_CONFIG_MODULE')

class SqlAlchemyTask(Task):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

@app.task(base=SqlAlchemyTask)
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


@app.task(base=SqlAlchemyTask)
def scrape():
    Scraper().fetch_and_persist(db_session)

@app.task(base=SqlAlchemyTask)
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

