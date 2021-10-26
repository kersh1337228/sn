# Generated by Django 3.2.7 on 2021-10-25 17:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_media', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_community', '0001_initial'),
        ('user_note', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='audios',
            field=models.ManyToManyField(related_name='community_audios', to='user_media.Audio'),
        ),
        migrations.AddField(
            model_name='community',
            name='files',
            field=models.ManyToManyField(related_name='community_files', to='user_media.File'),
        ),
        migrations.AddField(
            model_name='community',
            name='images',
            field=models.ManyToManyField(related_name='community_images', to='user_media.Image'),
        ),
        migrations.AddField(
            model_name='community',
            name='notes',
            field=models.ManyToManyField(related_name='community_notes', to='user_note.Note'),
        ),
        migrations.AddField(
            model_name='community',
            name='reposts',
            field=models.ManyToManyField(related_name='community_reposts', to='user_note.Note'),
        ),
        migrations.AddField(
            model_name='community',
            name='staff_list',
            field=models.ManyToManyField(related_name='staff_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='subscribe_requests',
            field=models.ManyToManyField(related_name='subscribe_requests', to='user_community.CommunitySubscribeRequest'),
        ),
        migrations.AddField(
            model_name='community',
            name='videos',
            field=models.ManyToManyField(related_name='community_videos', to='user_media.Video'),
        ),
    ]
