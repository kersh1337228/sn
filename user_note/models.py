from django.contrib.auth import get_user_model
from django.db import models
from .utils import PostMixin


User = get_user_model()


'''
Note left by user or community,
contains content, publish information and
statistics.
'''
class Note(PostMixin, models.Model):
    '''Statistics'''
    comments_amount = models.PositiveIntegerField(
        verbose_name='Comments',
        blank=True,
        default=0
    )
    reposts_amount = models.PositiveIntegerField(
        verbose_name='Reposts',
        blank=True,
        default=0
    )
    images = models.ManyToManyField(
        'user_media.Image',
        related_name='note_images',
    )
    videos = models.ManyToManyField(
        'user_media.Video',
        related_name='note_videos',
    )
    audios = models.ManyToManyField(
        'user_media.Audio',
        related_name='note_audios',
    )
    files = models.ManyToManyField(
        'user_media.File',
        related_name='note_files',
    )


'''
User or community comment 
or a reply to an other comment.
'''
class Comment(PostMixin, models.Model):
    '''Is a reply to another commentary or not'''
    replies_to = models.ForeignKey(
        'Comment',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    '''Media'''
    images = models.ManyToManyField(
        'user_media.Image',
        related_name='comment_images',
    )
    videos = models.ManyToManyField(
        'user_media.Video',
        related_name='comment_videos',
    )
    audios = models.ManyToManyField(
        'user_media.Audio',
        related_name='comment_audios',
    )
    files = models.ManyToManyField(
        'user_media.File',
        related_name='comment_files',
    )
    '''Statistics'''
    replies_amount = models.PositiveIntegerField()


'''
Repost to user or community 
page made by the last one listed.
'''
class Repost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )


'''Like set be user or community'''
class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
