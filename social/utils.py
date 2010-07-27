def filter_permitted_fields(obj, owner, requesting_user):
    fields = obj._meta.fields
    # Attach our user to the object so we can check permission in has_field_perm.
    # This is a hack but is required since we can't pass a user though has_field_perm.
    obj.target_user = owner

    filtered_dict = {}
    for field in fields:
        if requesting_user.has_field_perm(perm='view', obj=obj, field=field):
            filtered_dict[field.name] = getattr(obj, field.name)

    return filtered_dict

def filter_permitted_objects(object_list, owner, requesting_user, count=None):
    filtered_list = []

    for obj in object_list:
        # Attach our user to the object so we can check permission in has_perm.
        # This is a hack but is required since we can't pass a user though has_perm.
        obj.target_user = owner
        if requesting_user.has_perm(perm='view', obj=obj):
            filtered_list.append(obj)
            if count:
                if len(filtered_list) >= count:
                    break

    return filtered_list


def put_wall_post_comment(sender, instance, created, **kwargs):
    import pdb; pdb.set_trace()

    posting_user = instance.user


    
    attch = { 
        "name": "Link name", 
        "link": "http://www.example.com/",
        "caption": "{*actor*} posted a new review",
        "description": "This is a longer description of the attachment",
        "picture": "http://www.example.com/thumbnail.jpg"
    }

    context['request'].facebook.graph.put_wall_post('message', attachment=attch)

from django.db.models.signals import post_save
from django.contrib.comments.models import Comment

post_save.connect(put_wall_post_comment, sender=Comment)
