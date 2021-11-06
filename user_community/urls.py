from django.urls import path

from user.views import like_view
from user_community.views import CommunityCreateView, CommunityPageView, CommunityListView, \
    CommunityEditView, CommunityDeleteView, subscribe_view, unsubscribe_view

urlpatterns = [
    # Community page
    path(
        'community/<slug:community_id>/',
        CommunityPageView.as_view(),
        name='community_page'
    ),
    # Community list page
    path(
        'list/',
        CommunityListView.as_view(),
        name='community_list'
    ),
    # Community creation page
    path(
        'create/',
        CommunityCreateView.as_view(),
        name='community_create'
    ),
    # Community edit page
    path(
        'edit/<slug:community_id>/',
        CommunityEditView.as_view(),
        name='community_edit'
    ),
    # Community delete page
    path(
        'delete/<slug:community_id>/',
        CommunityDeleteView.as_view(),
        name='community_delete'
    ),
    path(
        'subscribe/<slug:community_id>/',
        subscribe_view,
        name='community_subscribe'
    ),
    path(
        'unsubscribe/<slug:community_id>/',
        unsubscribe_view,
        name='community_unsubscribe'
    ),
]