from datetime import datetime

from celery import Celery
from celery import Task

from scraper import Scraper
from models import Tweet
from app.main import db_session, twitter_api


app = Celery("twitterbot")
app.config_from_envvar('CELERY_CONFIG_MODULE')

class SqlAlchemyTask(Task):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@app.task(base=SqlAlchemyTask)
def scrape():
    Scraper().fetch_and_persist(db_session)

@app.task(base=SqlAlchemyTask)
def tweet():
    tweet = db_session.query(Tweet).filter_by(posted=None).first()
    if tweet is not None:
        tweet.post_to_twitter(twitter_api)
        tweet.posted = datetime.now()
        db_session.commit()
    else:
        scrape().delay()

