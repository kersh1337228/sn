import re
from django.core.exceptions import ValidationError


def validate_community_name(name):
    community_name_regular = r'^[\w ]+$'
    if not re.match(community_name_regular, name):
        raise ValidationError(
            f'Wrong community name format',
            code='wrong_community_name',
        )


def get_community_state(authorized_user, community):
    if authorized_user in community.staff_list.all():
        return 'staff_community_page'
    elif community in authorized_user.community_subscribes.all():
        if community.is_public:
            return 'subscription_public_community_page'
        else:
            return 'subscription_private_community_page'
    else:
        subscribe_requests_list = [
            request.from_user for request in community.subscribe_requests.all()
        ]
        if authorized_user in subscribe_requests_list:
            return 'request_private_community_page'
        else:
            if community.is_public:
                return 'public_community_page'
            else:
                return 'private_community_page'
