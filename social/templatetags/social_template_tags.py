from django import template
from django.template import TemplateSyntaxError

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

        filtered_object = obj
        if self.as_var:
            context[self.as_var] = filtered_object
            return ''
        else:
            return filtered_object
