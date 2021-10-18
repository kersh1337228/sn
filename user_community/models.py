from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


'''
User community model, 
realizing multi-person structures.
'''
class Community(models.Model):
    community_id = models.SlugField(
        verbose_name='Community ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )
    creation_date = models.DateField(
        verbose_name='Creation date',
        null=False,
        blank=False,
        auto_now_add=True
    )
    is_public = models.BooleanField(
        verbose_name='Private or Public community',
        null=False,
        blank=False,
        default=False,
        choices=[
            (True, 'Public'),
            (False, 'Private'),
        ]
    )

    '''Subscriptions'''
    subscribers = models.ManyToManyField(
        User,
        blank=True,
    )

    '''Community Personal Data'''

    website = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    about = models.TextField(
        verbose_name='About me',
        max_length=32767,
        null=True,
        blank=True,
        default=None,
    )


'''
Community subscriber model, 
realizing user-to-community subscription model.
'''
class CommunitySubscriber(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_community',
    )
    subscribed_to_community = models.ForeignKey(
        'Community',
        on_delete=models.CASCADE,
        related_name='follower'
    )
