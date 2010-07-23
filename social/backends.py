from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from social.constants import SOCIAL_GROUPS
from social.models import SocialObjectPermission, SocialObjectFieldPermission, resolve_is_member_method

class SocialObjectPermissionBackend(object):
    """
    Authentication backend providing a social permissions system, 
    i.e. which users (friends included) can access another's content.
    """
    supports_object_permissions=True
    supports_anonymous_user=True

    def authenticate(self, username, password):
        """
        We don't care about authentication here, so return None.
        """
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user has access to object based on social permissions.
        """
        # if no object is provided then we assume we don't have access
        if obj is None:
            return False

        # get object's content type
        content_type = ContentType.objects.get_for_model(obj)

        # try to resolve the required permission name. if we can't resolve one we assume we don't have access
        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        # get our user against which to check permission
        target_user=obj.target_user

        # get configured social permission objects by content type, permission and owner.
        # iterate over result and check if user is part of the social group. 
        # if so permission is granted.
        perms = SocialObjectPermission.objects.filter(content_type=content_type, user=target_user).filter(**{'can_%s' % perm: True})

        # permissions take priority by social group id, with lowest ids being of highest priority
        perms = perms.order_by('social_group')
        for perm in perms:
            return perm.is_member(target_user=target_user, requesting_user=user_obj)
        
        # fallback to default social group if we could not determine permission.
        # if no default is defined, raise an ImproperlyConfigured exception.
        try:
            default_social_group = settings.DEFAULT_SOCIAL_PERMISSION_GROUP
            return resolve_is_member_method(SOCIAL_GROUPS[default_social_group][1])(target_user=target_user, requesting_user=user_obj)
        except AttributeError:
            raise ImproperlyConfigured('settings should provide a DEFAULT_SOCIAL_PERMISSION_GROUP.')

class SocialObjectFieldPermissionBackend(object):
    """
    Authentication backend providing a social permissions system, 
    i.e. which users (friends included) can access another's content.
    """
    supports_field_permissions=True
    supports_anonymous_user=True

    def authenticate(self, username, password):
        """
        We don't care about authentication here, so return None.
        """
        return None

    def has_field_perm(self, user_obj, perm, obj=None, field=None):
        """
        Check if user has access to object based on social permissions.
        """
        # if no field or object is provided then we assume we don't have access
        if field is None or obj is None:
            return False

        # get object's content type
        content_type = ContentType.objects.get_for_model(obj)

        # try to resolve the required permission name. if we can't resolve one we assume we don't have access
        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        # get our user against which to check permission
        target_user=obj.target_user

        # get configured social permission objects by content type, permission and owner.
        # iterate over result and check if user is part of the social group. 
        # if so permission is granted.
        perms = SocialObjectFieldPermission.objects.filter(content_type=content_type, field_name=field.name, user=target_user).filter(**{'can_%s' % perm: True})

        # permissions take priority by social group id, with lowest ids being of highest priority
        perms = perms.order_by('social_group')
        for perm in perms:
            return perm.is_member(target_user=target_user, requesting_user=user_obj)
        
        # fallback to default social group if we could not determine permission.
        # if no default is defined, raise an ImproperlyConfigured exception.
        try:
            default_social_group = settings.DEFAULT_SOCIAL_PERMISSION_GROUP
            return resolve_is_member_method(SOCIAL_GROUPS[default_social_group][1])(target_user=target_user, requesting_user=user_obj)
        except AttributeError:
            raise ImproperlyConfigured('settings should provide a DEFAULT_SOCIAL_PERMISSION_GROUP.')
