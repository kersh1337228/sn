from django import template


register = template.Library()


@register.inclusion_tag('current_user_message.html')
def current_user_message_tag(**kwargs):
    return kwargs


@register.inclusion_tag('other_user_message.html')
def other_user_message_tag(**kwargs):
    return kwargs