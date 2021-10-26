from django.contrib import admin
from user_chat.models import PrivateChat, GroupChat


admin.site.register(PrivateChat)
admin.site.register(GroupChat)
