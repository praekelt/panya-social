from django.contrib.comments.models import Comment

from panya.models import ModelBase
from panya.utils import modify_class

class CommentModifier(object):
    """
    Modifies comment class to include a get_owner method for use with the SocialObjectPermissionBackend.
    """
    def get_owner(self):
        """
        return comment creating user
        """
        return self.user

class ModelBaseModifier(object):
    """
    Modifies MOdelBase class to include a get_owner method for use with the SocialObjectPermissionBackend.
    """
    def get_owner(self):
        """
        return object owner
        """
        return self.owner

modify_class(Comment, CommentModifier)
modify_class(ModelBase, ModelBaseModifier)
