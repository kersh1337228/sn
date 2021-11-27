from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView

from user.views import functionally_based_view_decorator
from user_friend.models import UserFriendRequest, Friend


User = get_user_model()


'''View of current user friend list'''
class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'friend_list.html'
    context_object_name = 'friend_list'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            friends_html = ''
            friend_list = []
            if request.GET.get('search'):
                friend_list = request.user.friends.annotate(
                    friend_full_name=Concat(
                        'first_name',
                        Value(' '),
                        'last_name',
                    )
                ).filter(
                    friend_full_name__icontains=request.GET.get('search')
                )
            else:
                friend_list = request.user.friends.all()
            if friend_list:
                for friend in friend_list:
                    friends_html += render_to_string(
                        'friend_min.html',
                        {
                            'friend': friend,
                            'request': request,
                        }
                    )
            else:
                friends_html = 'No matching friends'
            return JsonResponse({'friends': friends_html}, status=200)
        else:
            return super(FriendListView, self).get(request, *args, **kwargs)

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
@functionally_based_view_decorator
def friend_request_result(request, user_id, result):
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
    return redirect(request.META['HTTP_REFERER'])


'''View of sending friend request'''
@login_required
@functionally_based_view_decorator
def add_friend_view(request, friend_id):
    friend = get_object_or_404(User, user_id=friend_id)
    friend_request = UserFriendRequest(
            from_user=request.user,
            to_user=friend,
            state=None,
        )
    friend_request.save()
    friend.friend_requests.add(friend_request)
    return redirect(request.META['HTTP_REFERER'])


'''View of deleting user from your friend list'''
@login_required
@functionally_based_view_decorator
def delete_friend_view(request, friend_id):
    friend = get_object_or_404(User, user_id=friend_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])