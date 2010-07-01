from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from social.constants import SOCIAL_GROUPS

def is_member_everyone(target_user, requesting_user):
    """
    Always return True. All users are part of 'Everyone'.
    """
    return True

def is_member_nobody(target_user, requesting_user):
    """
    Always return False. No users are part of 'Nobody'.
    """
    return False
    
class SocialObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()
    social_group = models.IntegerField(
        choices = SOCIAL_GROUPS,
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def is_member(self, target_user, requesting_user):
        """
        Determine if the requesting user is part of the social group this permission applies to.
        """
        options = {
            'Everyone': is_member_everyone,
            'Nobody': is_member_nobody,
        }
        return options[SOCIAL_GROUPS[self.social_group][1]](context)
