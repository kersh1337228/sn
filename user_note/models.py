import datetime

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

    def save(self, *args, **kwargs):
        if not self.note_id:
            now = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            if self.user:
                self.note_id = f'{self.user.user_id}_note_{now}'
            else:
                self.note_id = f'{self.community.community_id}_note_{now}'
        super(Note, self).save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if not self.comment_id:
            now = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            self.comment_id = f'{self.note_commented.note_id}_comment_{now}'
        super(Comment, self).save(*args, **kwargs)


'''Reply to another comment.'''
class Reply(PostMixin):
    comment_replied = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comment_replied'
    )
    '''id'''
    reply_id = models.SlugField(
        verbose_name='Reply ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.reply_id:
            now = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            self.reply_id = f'{self.comment_replied.comment_id}_reply_{now}'
        super(Reply, self).save(*args, **kwargs)

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


'''Like set by user'''
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
    reply = models.ForeignKey(
        Reply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='like_to_reply'
    )

    class Meta:
        unique_together = (
            'user',
            'note',
            'comment',
            'reply'
        )
