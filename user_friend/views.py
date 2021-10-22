from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from user_friend.models import UserFriendRequest, Friend


User = get_user_model()


'''View of current user friend list'''
class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'friend_list.html'
    context_object_name = 'friend_list'

    def get_queryset(self):
        return self.request.user.friends.all()


'''View of current user friend request list'''
class FriendRequestListView(LoginRequiredMixin, ListView):
    model = UserFriendRequest
    template_name = 'friend_requests.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
        return self.request.user.friend_requests.all()


'''View of answering on friend request'''
@login_required
def friend_request_result(request, user_id, result):
    if request.user.is_active:
        current_user = request.user
        request_user = get_object_or_404(User, user_id=user_id)
        if result == 'accept':
            friend = Friend(
                from_user=request_user,
                to_user=current_user,
            )
            friend.save()
            current_user.friends.add(request_user)
        current_user.friend_requests.get(from_user=request_user).delete()
        return redirect('friend_requests')
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)


'''View of sending friend request'''
@login_required
def add_friend_view(request, friend_id):
    if request.user.is_active:
        Friend = get_object_or_404(User, user_id=friend_id)
        friend_request = UserFriendRequest(
                from_user=request.user,
                to_user=Friend,
                state=None,
            )
        friend_request.save()
        Friend.friend_requests.add(friend_request)
        return redirect('user_page', friend_id)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)
