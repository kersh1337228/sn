from django import template


register = template.Library()


@register.inclusion_tag('profile_actions.html')
def profile_actions_tag(user, authorised_user_state):
    return {
        'user': user,
        'authorised_user_state': authorised_user_state,
    }


@register.inclusion_tag('attach_content.html')
def attach_content_tag():
    return {}


@register.inclusion_tag('note.html')
def note_tag(user, note, comment_add_form):
    return {
        'user': user,
        'note': note,
        'comment_add_form': comment_add_form,
    }


@register.inclusion_tag('comment.html')
def note_tag(user, note, comment_add_form):
    return {
        'user': user,
        'note': note,
        'comment_add_form': comment_add_form,
    }
