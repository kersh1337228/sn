from django.urls import path
from user_community.views import CommunityCreateView, CommunityPageView, CommunityListView, \
    CommunityEditView, CommunityDeleteView, subscribe_view, unsubscribe_view

urlpatterns = [
    path(
        'community/<slug:community_id>/',
        CommunityPageView.as_view(),
        name='community_page'
    ),
    path(
        'list/',
        CommunityListView.as_view(),
        name='community_list'
    ),
    path(
        'create/',
        CommunityCreateView.as_view(),
        name='community_create'
    ),
    path(
        'edit/<slug:community_id>/',
        CommunityEditView.as_view(),
        name='community_edit'
    ),
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