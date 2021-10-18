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
    text = models.TextField(blank=True, verbose_name='Text')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='Published')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Last updated')
    # User, who has published the note.
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    # Community which has published the note.
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)

    '''Statistics'''
    likes_amount = models.PositiveIntegerField(verbose_name='Likes', blank=True, default=0)

    def __str__(self):
        return self.text[:50]