from django.contrib.auth import get_user_model
from django.db import models
from .utils import PostMixin
from user_media.models import Image, Video, Audio, File


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


'''
Note image separate model, 
allowing to upload multiple images to one note.
'''
class NoteImage(Image, models.Model):
    note = models.ForeignKey(
        'Note',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )


'''
Note video model, 
allowing to upload video files to note.
'''
class NoteVideo(Video, models.Model):
    note = models.ForeignKey(
        'Note',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )


'''
Note audio model, 
allowing to upload audio files to note.
'''
class NoteAudio(Audio, models.Model):
    note = models.ForeignKey(
        'Note',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

'''
Note file separate model, 
allowing to upload multiple files to one note.
'''
class NoteFile(File, models.Model):
    note = models.ForeignKey(
        'Note',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
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
