from django import template


register = template.Library()


@register.inclusion_tag('friend_min.html')
def friend_min_tag(**kwargs):
    return kwargs


@register.inclusion_tag('friend_request_min.html')
def friend_request_min_tag(**kwargs):
    return kwargs
