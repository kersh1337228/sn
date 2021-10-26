from django.contrib.auth import get_user_model
from django.db import models
from user_community.models import Community
from user_media.models import Image, Video, Audio, File


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
    likes_amount = models.PositiveIntegerField(
        verbose_name='Likes',
        blank=True,
        default=0
    )

    def __str__(self):
        return self.text[:50]


'''Function helping to attach multiple media files to one note'''
def note_attach_media(objects, type, owner_type, owner, note):
    if objects:
        if type == 'image':
            if owner_type == 'user':
                for image in objects:
                    img = Image(
                        image=image,
                        user=owner,
                    )
                    img.save()
                    note.images.add(img)
            elif owner_type == 'community':
                for image in objects:
                    img = Image(
                        image=image,
                        community=owner,
                    )
                    img.save()
                    note.images.add(img)
        elif type == 'video':
            if owner_type == 'user':
                for video in objects:
                    vid = Video(
                        video=video,
                        user=owner,
                    )
                    vid.save()
                    note.videos.add(vid)
            elif owner_type == 'community':
                for video in objects:
                    vid = Image(
                        video=video,
                        community=owner,
                    )
                    vid.save()
                    note.images.add(vid)
        elif type == 'audio':
            if owner_type == 'user':
                for audio in objects:
                    aud = Audio(
                        audio=audio,
                        user=owner,
                    )
                    aud.save()
                    note.audios.add(aud)
            elif owner_type == 'community':
                for audio in objects:
                    aud = Audio(
                        audio=audio,
                        community=owner,
                    )
                    aud.save()
                    note.audios.add(aud)
        elif type == 'file':
            if owner_type == 'user':
                for file in objects:
                    fil = File(
                        file=file,
                        user=owner,
                    )
                    fil.save()
                    note.images.add(fil)
            elif owner_type == 'community':
                for file in objects:
                    fil = File(
                        file=file,
                        community=owner,
                    )
                    fil.save()
                    note.images.add(fil)
    return note
