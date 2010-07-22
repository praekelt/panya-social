import random

from django import template

from friends.models import Friendship, FriendshipInvitation

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
def friendship_setup_button(context, user):
    """
    Renders either an 'add friend', 'remove friend' or 'awaiting confirmation' button based on current friendship state.
    Also includes javascript to request friend or remove friend.
    """
    # Render add friend template by default.
    include_template = 'social/inclusion_tags/friendship_add_button.html'
    requesting_user = context['request'].user

    if requesting_user.is_authenticated():
        # If users are friends already render remove friend template.
        are_friends = Friendship.objects.are_friends(requesting_user, user)
        if are_friends:
            include_template = 'social/inclusion_tags/friendship_remove_button.html'
        else:
            # If users are not friends but an invitation exists, render awaiting confirmation template.
            status = FriendshipInvitation.objects.invitation_status(user1=requesting_user, user2=user)
            if status == 2:
                include_template = 'social/inclusion_tags/friendship_awaiting_confirmation_button.html'

    return {
        'include_template': include_template,
        'object': user,
    }
