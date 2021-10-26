# Generated by Django 3.2.7 on 2021-10-25 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_media', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='audios',
            field=models.ManyToManyField(related_name='message_image', to='user_media.Audio'),
        ),
        migrations.AddField(
            model_name='message',
            name='files',
            field=models.ManyToManyField(related_name='message_image', to='user_media.File'),
        ),
        migrations.AddField(
            model_name='message',
            name='images',
            field=models.ManyToManyField(related_name='message_image', to='user_media.Image'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='videos',
            field=models.ManyToManyField(related_name='message_image', to='user_media.Video'),
        ),
        migrations.AddField(
            model_name='groupchat',
            name='members',
            field=models.ManyToManyField(related_name='group_chat_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupchat',
            name='messages',
            field=models.ManyToManyField(related_name='group_chat_messages', to='user_chat.Message'),
        ),
    ]
