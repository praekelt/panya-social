import random

from django import template
from django.conf import settings
from django.contrib.sites.models import Site

from friends.models import Friendship, FriendshipInvitation
from socialregistration.models import FacebookProfile

register = template.Library()

@register.inclusion_tag('social/inclusion_tags/twitter_connect_form.html', takes_context=True)
def twitter_connect_form(context, form_id):
    context.update({
        'form_id': form_id,
    })
    return context

@register.inclusion_tag('social/inclusion_tags/facebook_connect_form.html', takes_context=True)
def facebook_connect_form(context, form_id):
    context.update({
        'form_id': form_id,
    })
    return context

@register.inclusion_tag('social/inclusion_tags/twitter_connect_button.html')
def twitter_connect_button(form_id, media_path):
    return {
        'form_id': form_id,
        'media_path': media_path,
    }

@register.inclusion_tag('social/inclusion_tags/facebook_connect_button.html')
def facebook_connect_button(form_id, media_path):
    return {
        'form_id': form_id,
        'media_path': media_path,
    }

@register.inclusion_tag('social/inclusion_tags/friendship_setup_button.html', takes_context=True)
def friendship_setup_button(context, user, include_template_name='social/inclusion_tags/friendship_setup_button_include.html'):
    """
    Renders either an 'add friend', 'remove friend', 'awaiting confirmation' or 'friendship declined' button based on current friendship state.
    Also includes javascript to request friend or remove friend.
    """
    if not user:
        return {} 

    # Render add friend template by default.
    active_class = "add_friend"
    requesting_user = context['request'].user

    if requesting_user.is_authenticated():
        # If users are friends already render remove friend template.
        are_friends = Friendship.objects.are_friends(requesting_user, user)
        if are_friends:
            active_class = "remove_friend"
        else:
            # If users are not friends but an invitation exists, render awaiting confirmation or declined template.
            status = FriendshipInvitation.objects.invitation_status(user1=requesting_user, user2=user)
            if status == 2:
                active_class = "awaiting_friend_confirmation"
            if status == 6:
                active_class = "request_declined"

    return {
        'include_template_name': include_template_name,
        'object': user,
        'active_class': active_class,
        'random': random.randint(0, 100000000)
    }

@register.inclusion_tag('social/inclusion_tags/facebook_invite_friends.html', takes_context=True)
def facebook_invite_friends(context, user):
    """
    Renders Facebook friends invite form.
    """
    current_site = Site.objects.get(id=settings.SITE_ID)

    # exclude id's of facebook users that are already using the app
    fb_profiles = FacebookProfile.objects.all()
    exclude_ids = ",".join([fb_profile.uid for fb_profile in fb_profiles])

    return {
        'exclude_ids': exclude_ids,
        'site_name': current_site.name,
        'site_domain': current_site.domain,
        'next': context['next'],
    }
