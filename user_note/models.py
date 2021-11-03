from django.contrib.auth import get_user_model
from django.db import models

from user_community.models import Community

User = get_user_model()


'''
Mixin for use with objects,
that can be posted by user or community.
'''
class PostMixin(models.Model):
    '''Content'''
    text = models.TextField(
        blank=True,
        verbose_name='Text'
    )
    publish_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Published'
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Last updated'
    )
    # User, who has published the note.
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    # Community which has published the note.
    community = models.ForeignKey(
        Community,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    '''Statistics'''
    likes = models.ManyToManyField(
        'Like',
        related_name='note_likes'
    )
    liked_by = models.ManyToManyField(
        User,
        related_name='note_liked_by'
    )

    '''Media'''
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

    def __str__(self):
        return self.text[:50]


'''
Note left by user or community,
contains content, publish information and
statistics.
'''
class Note(PostMixin):
    comments = models.ManyToManyField(
        'Comment',
        related_name='note_comments'
    )
    '''Statistics'''
    reposts_amount = models.PositiveIntegerField(
        verbose_name='Reposts',
        blank=True,
        default=0
    )
    '''id'''
    note_id = models.SlugField(
        verbose_name='Note ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )


'''User or community comment'''
class Comment(PostMixin):
    replies = models.ManyToManyField(
        'Reply',
        related_name='comment_replies'
    )
    note_commented = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='commented_note'
    )
    '''id'''
    comment_id = models.SlugField(
        verbose_name='Comment ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )


'''Reply to another comment.'''
class Reply(Comment):
    replies_to = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reply_source'
    )
    '''id'''
    reply_id = models.SlugField(
        verbose_name='Reply ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )

'''
Repost to user or community 
page made by the last one listed.
'''
class Repost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


'''Like set be user or community'''
class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='like_to_note'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='like_to_comment'
    )
