from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator

import random


# User Models

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    followed_tags = models.ManyToManyField('Tag', through="TagFollowing")

    profile_picture = models.ImageField(upload_to='profile_images', editable=True, default="profile_images/Bone.png")

    user_tag = models.OneToOneField('UserTag', related_name="userprofile_user_tag", editable=False)
    institution_tag = models.ForeignKey('InstitutionTag', related_name='userprofile_institution_tag', editable=False)

    def can_post_to_inst_tag(self, instTag):
        # Checks if a user can post to an InstitutionTag
        return instTag == self.institution_tag

    def save(self, *args, **kwargs):
        institution = getInstitution(self.user.email)

        # Automatically add user tag and institution tag to the user
        self.user_tag = UserTag.objects.get_or_create(name=self.user.username)[0]
        self.institution_tag = InstitutionTag.objects.get_or_create(name=institution)[0]
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


class UserReset(models.Model):
    username = models.CharField(max_length=100)
    code = models.IntegerField(blank=False, default=999999)

    def __unicode__(self):
        return str(self.code)


# Comment Models

class Comment(models.Model):
    author = models.ForeignKey('UserProfile')
    post = models.ForeignKey('Post')
    creation_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __unicode__(self):
        return self.content


# Like Models

class Like(models.Model):
    author = models.ForeignKey('UserProfile')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.author)

    class Meta:
        abstract = True


class PostLike(Like):
    post = models.ForeignKey('Post')

    def __unicode__(self):
        return str(self.author) + " liked " + str(self.post)

    class Meta:
        # Prevent a user from liking a post twice
        unique_together = ('author', 'post',)


class CommentLike(Like):
    comment = models.ForeignKey('Comment')

    def __unicode__(self):
        return str(self.author) + " liked " + str(self.comment)

    class Meta:
        # Prevent a user from liking a comment twice
        unique_together = ('author', 'comment',)


# Post Models

class Post(models.Model):
    author = models.ForeignKey('UserProfile')
    creation_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    tags = models.ManyToManyField('Tag', through="PostTagging", null=False, blank=False)
    rating = models.FloatField(default=0)

    title = models.CharField(max_length=100)
    content = models.TextField()

    slug = models.SlugField(editable=False)
    anonymous = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

        # Tag the user automatically
        if not self.anonymous:
            PostTagging.objects.get_or_create(post=self, tag=self.author.user_tag)
        else:
            anonymousTag = Tag.objects.get_or_create(name='anonymous')[0]
            PostTagging.objects.get_or_create(post=self, tag=anonymousTag)

    def __unicode__(self):
        return self.title

# Tag Models

class PostTagging(models.Model):
    post = models.ForeignKey('Post')
    tag = models.ForeignKey('Tag')
    tagging_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField('UserProfile', through="TagFollowing", null=True)
    posts = models.ManyToManyField('Post', through="PostTagging", null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)

        # Custom arg, that if we've updated the description, it's not given a default one...
        update = kwargs.pop('update', None)
        if not update:
            self.genDescription()

        super(Tag, self).save(*args, **kwargs)

    def genDescription(self):
        self.description = "This is for discussing @" + self.name + "."


    def __unicode__(self):
        return self.name


class InstitutionTag(Tag):
    def genDescription(self):
        self.description = "Posting in this tag is restricted to @" + self.name + " students."


class UserTag(Tag):
    def genDescription(self):
        self.description = "This tag lists the posts of @" + self.name + "."


class TagFollowing(models.Model):
    user = models.ForeignKey('UserProfile')
    tag = models.ForeignKey('Tag')
    follow_date = models.DateTimeField(auto_now_add=True)


# Misc. Functions
def getInstitution(email):
    # Could be changed to return domain.ac.uk instead of *.ac.uk
    return email.split("@")[1]
