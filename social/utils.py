import threading

from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.template import Template

from secretballot.models import Vote

import facebook

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


def get_wall_post_attachment(obj, **kwargs):
    current_site = Site.objects.get(id=settings.SITE_ID)
    context = {
        'object': obj,
        'site_name': current_site.name,
        'site_domain': current_site.domain,
    }
    context.update(kwargs)
    context = template.Context(context)
    t = Template("{% load panya_inclusion_tags %}{% render_object object 'facebook_wall_post' %}")
    result = t.render(context)
    if result:
        return eval(result)

def get_user_graph(user):
    # get graph using fabebook profile token
    facebook_profiles = user.facebookprofile_set.all()
    if facebook_profiles:
        oauth_access_token = facebook_profiles[0].oauth_access_token
        return facebook.GraphAPI(oauth_access_token)
   
def put_wall_post_threaded(graph, message, attachment):
    thread_kwargs = {}
    if message:
        thread_kwargs.update({'message': message})
    if attachment:
        thread_kwargs.update({'attachment': attachment})
    try:
        # post to users wall using threading
        t = threading.Thread(target=graph.put_wall_post, kwargs=thread_kwargs)
        t.setDaemon(True)
        t.start()
    # Yes it's bad to except blindly, but we don't want Facebook to hold up anything.
    except:
        pass
    
def put_wall_post_comment(sender, instance, created, **kwargs):
    if instance.user:
        if instance.user.is_authenticated():
            graph = get_user_graph(instance.user)
            if graph:
                attachment = get_wall_post_attachment(obj=instance.content_object, comment=instance.comment)
                put_wall_post_threaded(graph=graph, message='commented on KFC', attachment=attachment)

post_save.connect(put_wall_post_comment, sender=Comment)

def put_wall_post_vote(sender, instance, created, **kwargs):
    try:
        user = User.objects.get(username=instance.token)
    except User.DoesNotExist:
        return
    if user.is_authenticated():
        graph = get_user_graph(user)
        if graph:
            attachment = get_wall_post_attachment(obj=instance.content_object)
            put_wall_post_threaded(graph=graph, message='voted on KFC', attachment=attachment)

post_save.connect(put_wall_post_vote, sender=Vote)
