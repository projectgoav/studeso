from models import UserProfile, InstitutionTag, UserTag, Post, PostTagging, Tag
from django.contrib.auth.models import User
from django.test import TestCase


# Model tests
class UserProfileTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_student', password='test', email='test@student.gla.ac.uk')
        UserProfile.objects.create(user=test_user)

    def test_institution_tag_auto_created(self):
        try:
            InstitutionTag.objects.get(name='student.gla.ac.uk')
        except InstitutionTag.DoesNotExist:
            self.fail("Institution tag not auto created properly")

    def test_institution_tag_assignment(self):
        test_user = User.objects.get(username='test_student')
        test_user_profile = UserProfile.objects.get(user=test_user)

        self.assertEquals(test_user_profile.institution_tag, InstitutionTag.objects.get(name='student.gla.ac.uk'))

    def test_can_post_to_tag(self):
        test_user = User.objects.get(username='test_student')
        test_user_profile = UserProfile.objects.get(user=test_user)
        inst_tag = InstitutionTag.objects.get(name='student.gla.ac.uk')
        other_inst_tag = InstitutionTag.objects.create(name='uws.ac.uk')

        self.assertTrue(test_user_profile.canPostToTag(inst_tag))
        self.assertFalse(test_user_profile.canPostToTag(other_inst_tag))

    def test_user_tag_auto_creation(self):
        try:
            UserTag.objects.get(name='test_student')
        except UserTag.DoesNotExist:
            self.fail("Institution tag not auto created properly")

    def test_user_tag_assignment(self):
        test_user = User.objects.get(username='test_student')
        test_user_profile = UserProfile.objects.get(user=test_user)

        self.assertEquals(test_user_profile.user_tag, UserTag.objects.get(name='test_student'))


class PostTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_student', password='test', email='test@student.gla.ac.uk')
        test_user_profile = UserProfile.objects.create(user=test_user)
        Post.objects.create(author=test_user_profile, title="Testing in Django", content="Test content here")

    def test_post_with_negative_views(self):
        test_user = User.objects.get(username='test_student')
        test_user_profile = UserProfile.objects.get(user=test_user)

        post = Post.objects.create(author=test_user_profile, title='Django Testing', content='hello world', views=-10)
        self.assertEquals(post.views, 0)

    def test_slug_creation(self):
        post = Post.objects.get(title='Testing in Django')
        self.assertEquals(post.slug, 'testing-in-django')

    def test_author_auto_tagging(self):
        post = Post.objects.get(title='Testing in Django')

        try:
            tag = post.tags.get(name='test_student')
            PostTagging.objects.get(post=post, tag=tag)
        except UserTag.DoesNotExist:
            self.fail("Post not autotagged with author's UserTag correctly")
        except Tag.DoesNotExist:
            self.fail("Post not autotagged with author's UserTag correctly")

    def test_tagging(self):
        post = Post.objects.get(title='Testing in Django')
        tag = Tag.objects.create(name='testing')
        PostTagging.objects.create(post=post, tag=tag)

        try:
            tag = post.tags.get(name='testing')
            PostTagging.objects.get(post=post, tag=tag)
        except Tag.DoesNotExist:
            self.fail("Post not tagged correctly")
