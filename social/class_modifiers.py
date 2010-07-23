from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User

from panya.utils import modify_class

def _user_has_field_perm(user, perm, obj, field):
    anon = user.is_anonymous()
    for backend in auth.get_backends():
        if not anon or backend.supports_anonymous_user:
            if hasattr(backend, "has_field_perm"):
                if field is not None:
                    if (backend.supports_field_permissions and
                        backend.has_field_perm(user, perm, obj, field)):
                            return True
                else:
                    if backend.has_field_perm(user, perm):
                        return True
    return False

class UserModifier(object):
    """
    Modifies user class to include has_field_perm method used in a similar manner than has_perm, 
    except it checks field permissions as opposed to object permissions. 
    """
    def has_field_perm(self, perm, obj=None, field=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an field
        is provided, permissions for this specific field are checked.
        """
        # Inactive users have no permissions.
        if not self.is_active:
            return False

        # Superusers have all permissions.
        if self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_field_perm(self, perm, obj, field)
    
class AnonymousUserModifier(object):
    """
    Modifies user class to include has_field_perm method used in a similar manner than has_perm, 
    except it checks field permissions as opposed to object permissions. 
    """
    def has_field_perm(self, perm, obj=None, field=None):
        return _user_has_field_perm(self, perm, obj=obj, field=field)

modify_class(User, UserModifier)
modify_class(AnonymousUser, AnonymousUserModifier)
