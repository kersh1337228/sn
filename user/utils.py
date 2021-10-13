'''
Additional functions and mixins
'''
from django.contrib.auth import get_user_model


class UserViewMixin():
    def get_user_context(self, **kwargs):
        context = kwargs
        context['user'] = get_user_model()
        return context