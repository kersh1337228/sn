# Generated by Django 3.2.7 on 2021-11-06 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_community.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Community name')),
                ('community_id', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Community ID')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('is_public', models.BooleanField(choices=[(True, 'Public'), (False, 'Private')], default=True, verbose_name='Private or Public community')),
                ('preview_picture', models.ImageField(blank=True, upload_to=user_community.models.upload_to_community_picture)),
                ('website', models.URLField(blank=True, default=None, null=True, verbose_name='Website')),
                ('vk', models.URLField(blank=True, default=None, null=True, verbose_name='VK')),
                ('instagram', models.URLField(blank=True, default=None, null=True, verbose_name='Instagram')),
                ('facebook', models.URLField(blank=True, default=None, null=True, verbose_name='Facebook')),
                ('twitter', models.URLField(blank=True, default=None, null=True, verbose_name='Twitter')),
                ('about', models.TextField(blank=True, default=None, max_length=32767, null=True, verbose_name='About me')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommunitySubscribeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(choices=[(None, 'Await'), (True, 'Accepted'), (False, 'Rejected')], default=None, max_length=25, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_request_from', to=settings.AUTH_USER_MODEL)),
                ('to_community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_request_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunitySubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_community', to=settings.AUTH_USER_MODEL)),
                ('to_community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='user_community.community')),
            ],
        ),
    ]
