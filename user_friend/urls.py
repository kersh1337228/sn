from django.urls import path
from user_friend.views import add_friend_view, FriendRequestListView, FriendListView, friend_request_result, \
    delete_friend_view

urlpatterns = [
    # Current user friend list
    path(
        'friend_list/',
        FriendListView.as_view(),
        name='friend_list'
    ),
    path(
        'friend_list/search/',
        FriendListView.as_view(),
        name='friend_list_search'
    ),
    # Current user friend requests list
    path(
        'friend_requests/',
        FriendRequestListView.as_view(),
        name='friend_requests'
    ),
    # Friend request response
    path(
        'friend_requests/<slug:user_id>/<slug:result>/',
        friend_request_result,
        name='friend_requests_result'
    ),
    # Send friend request
    path(
        'add_friend/<slug:friend_id>/',
        add_friend_view,
        name='add_friend'
    ),
    # Delete user from current user's friend list
    path(
        'delete_friend/<slug:friend_id>/',
        delete_friend_view,
        name='delete_friend',
    )
]
