from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

from panya.models import ModelBase
from post.models import Post
from social import models

class CommentModifierTestCase(TestCase):
    def setUp(self):
        # create user and content
        self.owner = User.objects.create(username='test_user')
        self.comment = Comment(user=self.owner)
    
    def test_get_owner(self):
        self.failUnless(self.comment.get_owner(), self.owner)

class ModelBaseModifierTestCase(TestCase):
    def setUp(self):
        # create user and content
        self.owner = User.objects.create(username='test_user')
        self.modelbase = ModelBase(title='test_modelbase', owner=self.owner)
    
    def test_get_owner(self):
        self.failUnless(self.modelbase.get_owner(), self.owner)

class SocialObjectPermissionBackendTestCase(TestCase):
    fixtures=['users.json']    
    
    def setUp(self):
        # add our backend if not already there
        self.backend_str = 'social.backends.SocialObjectPermissionBackend'
        if self.backend_str not in settings.AUTHENTICATION_BACKENDS:
            settings.AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + (self.backend_str,)

        # create some users and content
        self.owner = User.objects.create(username='target_user')
        self.requesting_user = User.objects.create(username='requesting_user')
        self.post = Post.objects.create(title='Post Title', owner=self.owner)

    def test_has_perm(self):
        # TODO
        pass

    def test_is_member_everyone(self):
        # always retrun true
        self.failUnless(models.is_member_everyone(self.owner, self.requesting_user))
    
    def test_is_member_nobody(self):
        # always retrun false
        self.failIf(models.is_member_nobody(self.owner, self.requesting_user))
