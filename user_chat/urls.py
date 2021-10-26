from django.urls import path
from .views import PrivateChatView, GroupChatView, \
    create_private_chat_view, CreateGroupChatView, ChatListView


urlpatterns = [
    path('chat_list/', ChatListView.as_view(), name='chat_list'),
    path('private_chat/<slug:chat_id>/', PrivateChatView.as_view(), name='private_chat'),
    path('group_chat/<slug:chat_id>/', GroupChatView.as_view(), name='group_chat'),
    path('create/group_chat/', CreateGroupChatView.as_view(), name='create_group_chat'),
    path('create/private_chat/<slug:member_id>/', create_private_chat_view, name='create_private_chat'),
]