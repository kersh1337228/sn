from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


'''
Subscribe model, realizing 
user-to-user subscription.
'''
class Subscribe(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed',
    )


'''
Friend model, realizing
user-to-user friend relations.
'''
class Friend(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_user',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='frended',
    )


'''
FriendRequest model, realizing sending 
friend request before adding to friend list
'''
class UserFriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='request_from',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='request_to',
    )
    state = models.BooleanField(
        max_length=25,
        null=True,
        choices=[
            (None, 'Await'),
            (True, 'Accepted'),
            (False, 'Rejected'),
        ],
        default=None,
    )