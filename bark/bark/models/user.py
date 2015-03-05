from bark.bark.models.tag import InstitutionTag
from django.db import models
from django.contrib.auth.models import User
from bark.models.tag import Tag, UserTag, TagFollowing


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    followed_tags = models.ManyToManyField(Tag, through="TagFollowing")

    user_tag = models.OneToOneField(UserTag)
    institution_tag = models.ForeignKey(InstitutionTag)

    def canPostToTag(self, instTag):
        # Checks if a user can post to an InstitutionTag
        return instTag == self.institution_tag

    def save(self, *args, **kwargs):
        institution = getInstitution(self.user.email)
        self.user_tag = UserTag.objects.create(name=self.user.username)
        self.institution_tag = InstitutionTag.objects.get_or_create(name=institution)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


def getInstitution(email):
    # Could be changed to return domain.ac.uk instead of *.ac.uk
    return email.split("@")[1]
