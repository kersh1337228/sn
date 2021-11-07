'''
Additional functions and mixins
'''
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.views.generic import FormView


'''
Mixin class for user-app views,
contains template content getter
'''
class UserViewMixin():
    def get_user_context(self, **kwargs):
        context = kwargs
        return context


class UserEditMixin(LoginRequiredMixin, UserViewMixin, FormView):
    template_name = 'user_settings_form.html'
    success_url = reverse_lazy('user_settings')

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update(**model_to_dict(self.request.user))
        return initial

'''
Name validator for form 
first name and last name fields
'''
def validate_name(name, field):
    name_regular = r'^[A-ZА-Я]{1}[a-zа-я]+$'
    if not re.match(name_regular, name):
        raise ValidationError(
                f'Wrong {field} format',
                code='wrong_name',
            )


def get_user_state(current_user, authorized_user):
    if current_user.user_id == authorized_user.user_id:
        return 'authorized_user_page'
    else:
        if authorized_user in current_user.friends.all():
            return 'friend_user_page'
        else:
            if current_user in [request.from_user for request in authorized_user.friend_requests.all()]:
                return 'request_await_user_page'
            elif authorized_user in [request.from_user for request in current_user.friend_requests.all()]:
                if current_user.is_public:
                    return 'request_public_user_page'
                else:
                    return 'request_private_user_page'
            else:
                if current_user.is_public:
                    return 'public_user_page'
                else:
                    return 'private_user_page'
