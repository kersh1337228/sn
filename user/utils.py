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


def get_user_state(current_user, authorized_user):
    if current_user.user_id == authorized_user.user_id:
        return 'authorized_user_page'
    else:
        if authorized_user in current_user.friends.all():
            return 'friend_user_page'
        else:
            friend_requests_list = [
                request.from_user for request in current_user.friend_requests.all()
            ]
            if authorized_user in friend_requests_list:
                if current_user.is_public:
                    return 'request_public_user_page'
                else:
                    return 'request_private_user_page'
            else:
                if current_user.is_public:
                    return 'public_user_page'
                else:
                    return 'private_user_page'
