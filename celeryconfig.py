from datetime import timedelta
import os

BROKER_URL = os.environ['BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'tweet-every-1-hours': {
        'task': 'app.twitterbot.post_tweet',
        'schedule': timedelta(hours=1)
    },
    'follow-every-20-minutes': {
        'task': 'app.twitterbot.follow_based_on_last_tweet',
        'schedule': timedelta(minutes=20)
    }
}
