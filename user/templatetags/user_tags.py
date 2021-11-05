from django import template


register = template.Library()


@register.inclusion_tag('profile_actions.html')
def profile_actions_tag(**kwargs):
    return kwargs


@register.inclusion_tag('attach_content.html')
def attach_content_tag():
    return {}


@register.inclusion_tag('post.html')
def post_tag(**kwargs):
    return kwargs


@register.inclusion_tag('post_edit_menu.html')
def post_edit_menu_tag(**kwargs):
    return kwargs

@register.inclusion_tag('like.html')
def post_like_tag(**kwargs):
    return kwargs
