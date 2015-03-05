from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    followed_tags = models.ManyToManyField('Tag', through="TagFollowing")

    user_tag = models.OneToOneField('UserTag', related_name="userprofile_user_tag", editable=False)
    institution_tag = models.ForeignKey('InstitutionTag', related_name='userprofile_institution_tag', editable=False)

    def canPostToTag(self, instTag):
        # Checks if a user can post to an InstitutionTag
        return instTag == self.institution_tag

    def save(self, *args, **kwargs):
        institution = getInstitution(self.user.email)
        self.user_tag = UserTag.objects.create(name=self.user.username)
        self.institution_tag = InstitutionTag.objects.get_or_create(name=institution)[0]
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


class Comment(models.Model):
    author = models.ForeignKey('UserProfile')
    post = models.ForeignKey('Post')
    creation_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __unicode__(self):
        return self.content


class Like(models.Model):
    author = models.ForeignKey('UserProfile')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.author + "," + self.creation_date


class PostLike(Like):
    post = models.ForeignKey('Post')

    def __unicode__(self):
        return self.post + "," + super(Like, self)


class CommentLike(Like):
    comment = models.ForeignKey('Comment')

    def __unicode__(self):
        return self.comment + "," + super(Like, self)


class Post(models.Model):
    author = models.ForeignKey('UserProfile')
    creation_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', through="PostTagging", null=False, blank=False)
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
    post = models.ForeignKey('Post')
    tag = models.ForeignKey('Tag')
    tagging_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField('UserProfile', through="TagFollowing", null=True)
    posts = models.ManyToManyField('Post', through="PostTagging", null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Run clean()
        self.full_clean()
        self.genDescription()
        super(Tag, self).save(*args, **kwargs)

    def genDescription(self):
        self.description = "This is for discussing " + self.name + "."

    def clean(self):
        # Remove any spaces from name
        if self.name:
            self.name.replace(" ", "")

    def __unicode__(self):
        return self.name


class InstitutionTag(Tag):
    def genDescription(self):
        self.description = "Posting in this tag is restricted to " + self.name + " students."


class UserTag(Tag):
    def genDescription(self):
        self.description = "This tag lists the posts of " + self.name + "."


class TagFollowing(models.Model):
    user = models.ForeignKey('UserProfile')
    tag = models.ForeignKey('Tag')
    follow_date = models.DateTimeField(auto_now_add=True)


def getInstitution(email):
    # Could be changed to return domain.ac.uk instead of *.ac.uk
    return email.split("@")[1]