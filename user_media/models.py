from django.contrib.auth import get_user_model
from django.db import models
from user_community.models import Community


User = get_user_model()


'''
Image model allowing to upload, 
store and work with image-type media-files.
'''
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to=f'images/%Y/%m/%d')


'''
Video model allowing to upload, 
store and work with video-type media-files.
'''
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)
    video = models.FileField(upload_to=f'videos/%Y/%m/%d')


'''
Audio model allowing to upload, 
store and work with audio-type media-files.
'''
class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)
    audio = models.FileField(upload_to=f'audios/%Y/%m/%d')


'''
File model allowing to upload, 
store and work with general file-type media-files.
File model is made for either non-image or non-video or non-audio files.
'''
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)
    file = models.FileField(upload_to=f'files/%Y/%m/%d')
