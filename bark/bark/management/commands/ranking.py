from django.core.management.base import BaseCommand, CommandError
from math import log
from datetime import datetime
from bark.models import Post, PostLike
from django.utils.timezone import utc

# Can be accessed from python manage.py ranking

EPOCH = datetime(1970, 1, 1).replace(tzinfo=utc)
START_DATE = datetime(2015, 3, 9).replace(tzinfo=utc)


def seconds_since_epoch(date):
    """
    :param date: date of post
    :return: seconds since Unix epoch
    """
    seconds = date - EPOCH
    return seconds.total_seconds()


def rank(post):
    """
    Assigns a score to a post based on its number of likes and and the time
    since its creation

    Based on Reddit's hot ranking algorithm https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx
    :param post: post to be ranked
    """
    score = PostLike.objects.filter(post=post).count()
    order = log(max(abs(score), 1), 10)

    if score > 0:
        sign = 1
    elif score < 0:
        sign = -1
    else:
        sign = 0

    seconds = seconds_since_epoch(post.creation_date) - seconds_since_epoch(START_DATE)

    post.rating = round(sign * order + seconds / 45000, 7)


def rank_all():
    posts = Post.objects.all()

    for post in posts:
        rank(post)
        post.save()

    print "Ranking Complete: " + str(len(posts)) + " ranked."


class Command(BaseCommand):
    def handle(self, *args, **options):
        rank_all()
