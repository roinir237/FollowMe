import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import twitter

from config import app_config


db_engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=app_config.DEBUG)
db_session = scoped_session(sessionmaker(bind=db_engine))

os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

twitter_api = twitter.Api(consumer_key=app_config.TWITTER_KEY,
                          consumer_secret=app_config.TWITTER_SECRET,
                          access_token_key=app_config.TWITTER_ACCESS_TOKEN,
                          access_token_secret=app_config.TWITTER_TOKEN_SECRET)

