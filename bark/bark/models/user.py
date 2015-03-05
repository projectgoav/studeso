from django.db import models
from django.contrib.auth.models import User
from bark.models.tag import Tag, UserTag, TagFollowing


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    followed_tags = models.ManyToManyField(Tag, through="TagFollowing")


    # The tag created to link to the user
    user_tag = models.ForeignKey(UserTag, unique=True, default=user.username, editable=False)

    # Other stuff to be added later...

    def __unicode__(self):
        return self.user.username
