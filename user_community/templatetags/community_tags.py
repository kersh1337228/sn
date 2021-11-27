from django import template


register = template.Library()


@register.inclusion_tag('community_actions.html')
def community_actions_tag(**kwargs):
    return kwargs


@register.inclusion_tag('community_min.html')
def community_min_tag(**kwargs):
    return kwargs