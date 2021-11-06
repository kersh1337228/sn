from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


'''Function to create path for community preview pictures'''
def upload_to_community_picture(instance, filename):
    return f'{instance.community_id}/images/preview_pictures/%Y/%m/%d/{filename}'


'''
User community model, 
realizing multi-person structures.
'''
class Community(models.Model):
    '''Necessary community data'''
    name = models.CharField(
        verbose_name='Community name',
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )
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
        default=True,
        choices=[
            (True, 'Public'),
            (False, 'Private'),
        ]
    )
    '''Subscriptions are realized in user model'''
    subscribe_requests = models.ManyToManyField(
        'CommunitySubscribeRequest',
        related_name='subscribe_requests',
    )

    '''Notes, reposts and media'''
    notes = models.ManyToManyField(
        'user_note.Note',
        related_name='community_notes'
    )
    reposts = models.ManyToManyField(
        'user_note.Note',
        related_name='community_reposts'
    )
    images = models.ManyToManyField(
        'user_media.Image',
        related_name='community_images'
    )
    videos = models.ManyToManyField(
        'user_media.Video',
        related_name='community_videos'
    )
    audios = models.ManyToManyField(
        'user_media.Audio',
        related_name='community_audios'
    )
    files = models.ManyToManyField(
        'user_media.File',
        related_name='community_files'
    )


    '''Community Personal Data'''

    '''Community Basic Data'''
    preview_picture = models.ImageField(
        upload_to=upload_to_community_picture,
        blank=True,
    )
    '''Community contact data'''
    website = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    vk = models.URLField(
        verbose_name='VK',
        null=True,
        blank=True,
        default=None,
    )
    instagram = models.URLField(
        verbose_name='Instagram',
        null=True,
        blank=True,
        default=None,
    )
    facebook = models.URLField(
        verbose_name='Facebook',
        null=True,
        blank=True,
        default=None,
    )
    twitter = models.URLField(
        verbose_name='Twitter',
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
    '''Staff user list'''
    staff_list = models.ManyToManyField(
        User,
        related_name='staff_list',
    )
    '''Shows whether deleted or not'''
    is_active = models.BooleanField(
        default=True,
    )

    def get_absolute_url(self):
        return self.community_id

    def save(self, *args, **kwargs):
        if not self.community_id:
            self.community_id = self.name.replace(' ', '_').lower()
        super(Community, self).save(*args, **kwargs)

    def __str__(self):
        return self.community_id

'''
Community subscriber model, 
realizing user-to-community subscription model.
'''
class CommunitySubscriber(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_community',
    )
    to_community = models.ForeignKey(
        'Community',
        on_delete=models.CASCADE,
        related_name='followed'
    )


'''
CommunitySubscribeRequest model, realizing sending
subscribe request to private community before gaining
access to it's content
'''
class CommunitySubscribeRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe_request_from',
    )
    to_community = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe_request_to',
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
