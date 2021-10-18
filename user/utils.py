'''
Additional functions and mixins
'''
import re
from django.core.exceptions import ValidationError


'''
Mixin class for user-app views,
contains template content getter
'''
class UserViewMixin():
    def get_user_context(self, **kwargs):
        context = kwargs
        return context


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
