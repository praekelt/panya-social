class SocialObjectPermissionBackend(object):
    """
    Authentication backend providing a social permissions system, 
    i.e. which users (friends included) can access another's content.
    """
    supports_object_permissions=True
    supports_anonymous_user=True

    def authenticate(self, username, password):
        """
        We don't care about authentication here, so return None
        """
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        """
        # make sure we have a user, even if its anonymous
        if not user_obj.is_authenticated():
            user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

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

        # get our object's owner
        owner=obj.get_owner()

        # get configured social permission objects by content type, permission and owner
        # iterate over result and check if user is part of the social group. 
        # if so permission is granted
        perms = SocialObjectPermission.objects.filter(content_type=content_type, object_id=obj.id, permission=perm, user=owner)
        for perm in perms:
            #XXX:checkperm
            if perm.is_member(owner, user):
                return True

        # fallback to default social group if we could not determine permission
        default_social_group = settings.DEFAULT_SOCIAL_PERMISSION_GROUP
        return default_social_group.is_member(owner, user)
