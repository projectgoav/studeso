from django.db import models
from django.template.defaultfilters import slugify
from bark.models.tag import Tag
from user import UserProfile


class Post(models.Model):
    author = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, through="PostTagging")
    rating = 0.0

    title = models.CharField(max_length=100)
    content = models.TextField()

    slug = models.SlugField(editable=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class PostTagging(models.Model):
    post = models.ForeignKey(Post)
    tag = models.ForeignKey(Tag)
    tagging_date = models.DateTimeField(auto_now_add=True)
