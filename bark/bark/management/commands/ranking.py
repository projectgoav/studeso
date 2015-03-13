from django.core.management.base import BaseCommand
from math import log
from datetime import datetime
from bark.models import Post, PostLike
from django.db.transaction import atomic
from django.utils.timezone import utc

# Can be accessed from python manage.py ranking


def seconds_since_epoch(date):
    """
    :param date: date of post
    :return: seconds since Unix epoch
    """
    seconds = date - EPOCH
    return seconds.total_seconds()

EPOCH = datetime(1970, 1, 1).replace(tzinfo=utc)
START_DATE = datetime(2015, 3, 9).replace(tzinfo=utc)
SECONDS_SINCE_START = seconds_since_epoch(START_DATE)


def rank(post):
    """
    Assigns a score to a post based on its number of likes and and the time
    since its creation

    Based on Reddit's hot ranking algorithm https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx
    :param post: post to be ranked
    """
    score = post.postlike_set.filter(post=post).count()
    order = log(max(score, 1), 10)

    seconds = seconds_since_epoch(post.creation_date) - SECONDS_SINCE_START

    post.rating = round(order + seconds / 45000, 7)


@atomic
def rank_all():
    posts = Post.objects.all()

    for post in posts:
        rank(post)
        post.save()

    print "Ranking Complete: " + str(len(posts)) + " ranked."


class Command(BaseCommand):
    def handle(self, *args, **options):
        rank_all()
