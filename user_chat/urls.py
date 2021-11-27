from django.urls import path
from .views import PrivateChatView, GroupChatView, \
    create_private_chat_view, CreateGroupChatView, \
    ChatListView, PrivateChatEditMessageView, get_message_view, get_chats_view

urlpatterns = [
    path(
        'chat_list/',
        ChatListView.as_view(),
        name='chat_list'
    ),
    path(
        'chat_list/search/',
        ChatListView.as_view(),
        name='chat_list_search',
    ),
    path(
        'private_chat/<slug:chat_id>/',
        PrivateChatView.as_view(),
        name='private_chat'
    ),
    path(
        'edit/private_chat/<slug:chat_id>/<slug:message_id>/',
        PrivateChatEditMessageView.as_view(),
        name='private_chat_edit_message'
    ),
    path(
        'group_chat/<slug:chat_id>/',
        GroupChatView.as_view(),
        name='group_chat'
    ),
    path(
        'create/group_chat/',
        CreateGroupChatView.as_view(),
        name='create_group_chat'
    ),
    path(
        'create/private_chat/<slug:member_id>/',
        create_private_chat_view,
        name='create_private_chat'
    ),
    path(
        'get_message/<slug:chat_id>/<slug:message_id>/',
        get_message_view,
        name='get_message'
    ),
    path(
        'get_chats/',
        get_chats_view,
        name='get_chats'
    )
]