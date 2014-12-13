import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DB_URI']
    TWITTER_KEY = os.environ['TWITTER_KEY']
    TWITTER_SECRET = os.environ['TWITTER_SECRET']
    TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    TWITTER_TOKEN_SECRET = os.environ['TWITTER_TOKEN_SECRET']


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


env = os.environ['ENV']
app_config = Config

if env == "development":
    app_config = DevelopmentConfig
elif env == "production":
    app_config = ProductionConfig
