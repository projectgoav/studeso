from django.db import models
from bark.models.user import UserProfile
from bark.models.post import Post, PostTagging


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(UserProfile, through="TagFollowing")
    posts = models.ManyToManyField(Post, through="PostTagging")

    def save(self, *args, **kwargs):
        # Run clean()
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)

    def clean(self):
        # Remove any spaces from name
        if self.name:
            self.name.replace(" ", "")

    def __unicode__(self):
        return self.name


class TagFollowing(models.Model):
    user = models.ForeignKey(UserProfile)
    tag = models.ForeignKey(Tag)
    follow_date = models.DateTimeField(auto_now_add=True)
