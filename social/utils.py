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
