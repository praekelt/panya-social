from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import TemplateSyntaxError
from django.utils.http import urlencode

from social import utils

register = template.Library()

@register.tag
def filter_permitted_fields(parser, token):
    """
    Given an object and requesting user, filters(removes) fields based on users social permissions.
    """
    bits = token.split_contents()
    check_bits = bits[:-2] if 'as' in bits else bits
    if len(check_bits) < 4:
        raise TemplateSyntaxError("'%s' takes at least three arguments"
                                  " (object to filter, object owner and requesting user)" % bits[0])
    
    # prepare vars from bits
    obj = bits[1]
    owner = bits[2]
    requesting_user = bits[3]
    as_var = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        as_var = bits[-1]
    
    return FilterPermittedFieldsNode(obj, owner, requesting_user, as_var)

class FilterPermittedFieldsNode(template.Node):
    def __init__(self, obj, owner, requesting_user, as_var):
        self.obj = template.Variable(obj)
        self.owner = template.Variable(owner)
        self.requesting_user = template.Variable(requesting_user)
        self.as_var = as_var

    def render(self, context):
        obj = self.obj.resolve(context)
        owner = self.owner.resolve(context)
        requesting_user = self.requesting_user.resolve(context)

        filtered_object = utils.filter_permitted_fields(obj, owner, requesting_user)
        if self.as_var:
            context[self.as_var] = filtered_object
            return ''
        else:
            return filtered_object

@register.tag
def facebook_share_url(parser, token):
    """
    Given a path returns a Facebook sharing url.
    """
    bits = token.split_contents()
    check_bits = bits[:-2] if 'as' in bits else bits
    if len(check_bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least 1 argument"
                                  " (path to share)" % bits[0])
    
    # prepare vars from bits
    path = bits[1]
    as_var = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        as_var = bits[-1]
    
    return FacebookShareURLNode(path, as_var)

class FacebookShareURLNode(template.Node):
    def __init__(self, path, as_var):
        self.path = template.Variable(path)
        self.as_var = as_var

    def render(self, context):
        path = self.path.resolve(context)
    
        current_site = Site.objects.get(id=settings.SITE_ID)
        facebook_share_url = "http://www.facebook.com/sharer.php?%s" % urlencode({'u': 'http://%s%s' % (current_site.domain, path)})
    

        if self.as_var:
            context[self.as_var] = facebook_share_url
            return ''
        else:
            return facebook_share_url

@register.tag
def twitter_share_url(parser, token):
    """
    Given a path and message returns a Twitter sharing url with Tweet.
    """
    bits = token.split_contents()
    check_bits = bits[:-2] if 'as' in bits else bits
    if len(check_bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least 1 argument"
                                  " (path to share, twitter message)" % bits[0])
    
    # prepare vars from bits
    path = bits[1]
    message = bits[2]
    as_var = None
    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        as_var = bits[-1]
    
    return TwitterShareURLNode(path, message, as_var)

class TwitterShareURLNode(template.Node):
    def __init__(self, path, message, as_var):
        self.path = template.Variable(path)
        self.message = template.Variable(message)
        self.as_var = as_var

    def render(self, context):
        path = self.path.resolve(context)
        message = self.message.resolve(context)
    
        current_site = Site.objects.get(id=settings.SITE_ID)
        
        url = 'http://%s%s' % (current_site.domain, path)
        tweet = "%s...: %s" % (message[:140 - len(url) - 5], url)

        twitter_share_url = "http://twitter.com/home?%s" % urlencode({
            'status': tweet,
            'source': current_site.name
        })

        if self.as_var:
            context[self.as_var] = twitter_share_url
            return ''
        else:
            return twitter_share_url
