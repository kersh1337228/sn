import datetime
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


def upload_to_picture(instance, filename):
    now = datetime.datetime.now().strftime('%Y/%m/%d')
    return f'{instance.chat_id}/images/chat_picture/{now}/{filename}'


'''
Message model, allowing to send 
messages in chats and group chats
'''
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_sender'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Text',
    )
    publish_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Published'
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Last updated'
    )
    images = models.ManyToManyField(
        'user_media.Image',
        related_name='message_image',
    )
    videos = models.ManyToManyField(
        'user_media.Video',
        related_name='message_image',
    )
    audios = models.ManyToManyField(
        'user_media.Audio',
        related_name='message_image',
    )
    files = models.ManyToManyField(
        'user_media.File',
        related_name='message_image',
    )


class PrivateChat(models.Model):
    member_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='private_chat_member_1'
    )
    member_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='private_chat_member_2'
    )
    messages = models.ManyToManyField(
        'Message',
        related_name='private_chat_messages',
    )
    chat_id = models.SlugField(
        verbose_name='Chat ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.chat_id:
            self.chat_id = f'{self.member_1.user_id}_{self.member_2.user_id}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.chat_id

    def __str__(self):
        return self.chat_id


class GroupChat(models.Model):
    members = models.ManyToManyField(
        User,
        related_name='group_chat_members',
    )
    messages = models.ManyToManyField(
        'Message',
        related_name='group_chat_messages',
    )
    picture = models.ImageField(
        upload_to=upload_to_picture,
        blank=True,
    )
    staff = models.ManyToManyField(
        User,
        related_name='group_chat_staff',
    )
    name = models.CharField(
        verbose_name='Chat name',
        max_length=255,
        null=False,
        blank=False,
    )
    chat_id = models.SlugField(
        verbose_name='Chat ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.chat_id:
            data = self.clean_fields()
            self.chat_id = data.get('name').lower().replace('.', '_')

    def get_absolute_url(self):
        return self.chat_id

    def __str__(self):
        return self.chat_id
