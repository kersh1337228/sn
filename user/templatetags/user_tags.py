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
def comment_tag(user, comment, note, reply_add_form):
    return {
        'user': user,
        'comment': comment,
        'note': note,
        'reply_add_form': reply_add_form,
    }


@register.inclusion_tag('reply.html')
def reply_tag(user, note, comment, reply):
    return {
        'user': user,
        'note': note,
        'comment': comment,
        'reply': reply,
    }
