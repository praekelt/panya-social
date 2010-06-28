import random

from django import template
from socialregistration.utils import _https

register = template.Library()

@register.inclusion_tag('social/inclusion_tags/facebook_login_button.html', takes_context=True)
def facebook_login_button(context):
    context.update({
        'form_id': "facebook_login_form_%s" % random.randint(1,1000)
    })
    return context

@register.inclusion_tag('social/inclusion_tags/facebook_register_button.html', takes_context=True)
def facebook_register_button(context):
    context.update({
        'form_id': "facebook_register_form_%s" % random.randint(1,1000),
    })
    return context

@register.inclusion_tag('social/inclusion_tags/twitter_login_button.html', takes_context=True)
def twitter_login_button(context):
    context.update({
        'form_id': "twitter_login_form_%s" % random.randint(1,1000),
    })
    return context

@register.inclusion_tag('social/inclusion_tags/twitter_register_button.html', takes_context=True)
def twitter_register_button(context):
    context.update({
        'form_id': "twitter_register_form_%s" % random.randint(1,1000),
    })
    return context
