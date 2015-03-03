from django.db import models
from bark.models.post import Post
from bark.models.user import UserProfile


class Comment(models.Model):
    author = models.ForeignKey(UserProfile)
    post = models.ForeignKey(Post)
    creation_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __unicode__(self):
        return self.content
