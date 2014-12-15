from datetime import datetime

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
        # db_session.remove()


@app.task(base=SqlAlchemyTask)
def scrape():
    Scraper().fetch_and_persist(db_session)

@app.task(base=SqlAlchemyTask)
def tweet():
    msg = db_session.query(Tweet).filter_by(posted=None).first()
    if msg is not None:
        msg.post_to_twitter(twitter_api)
        msg.posted = datetime.now()
        db_session.commit()
    else:
        scrape().delay()

