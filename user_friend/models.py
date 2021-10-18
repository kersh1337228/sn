from django.db import models


'''
UserFriend model, realizing
user-to-user friend relations
'''
class UserFriend(models.Model):
    friend = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='friend_user',
    )
    friend_to_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='frended_user',
    )
