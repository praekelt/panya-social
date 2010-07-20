import random

from django import template
from socialregistration.utils import _https

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
