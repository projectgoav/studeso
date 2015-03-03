from django.db import models
from bark.models.comment import Comment
from bark.models.post import Post
from bark.models.user import UserProfile


class Like(models.Model):
    author = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.author + "," + self.creation_date


class PostLike(Like):
    like = models.ForeignKey(Like, unique=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return self.post + "," + super(Like, self)


class CommentLike(Like):
    like = models.ForeignKey(Like, unique=True)
    comment = models.ForeignKey(Comment)

    def __unicode__(self):
        return self.comment + "," + super(Like, self)
