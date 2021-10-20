from django.urls import path
from user_friend.views import add_friend_view, FriendRequestListView, FriendListView, friend_request_result

urlpatterns = [
    path('friend_list/', FriendListView.as_view(), name='friend_list'),
    path('friend_requests/', FriendRequestListView.as_view(), name='friend_requests'),
    path('friend_requests/<slug:user_id>/<slug:result>', friend_request_result, name='friend_requests_result'),
    path('add_friend/<slug:friend_id>', add_friend_view, name='add_friend'),
]
