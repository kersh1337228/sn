from django.urls import path

from user.views import like_view, delete_view
from user_community.views import CommunityCreateView, CommunityPageView, CommunityListView, \
    CommunityEditView, CommunityDeleteView, subscribe_view, unsubscribe_view, CommunityPageEditPostView

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
    # Community search list
    path(
        'list/search/',
        CommunityListView.as_view(),
        name='community_search_list'
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
    # Edit and delete

    # Notes
    path(
        'edit/community/<slug:community_id>/<slug:note_id>/',
        CommunityPageEditPostView.as_view(),
        name='community_page_edit_note'
    ),
    path(
        'delete/community/<slug:community_id>/<slug:note_id>/',
        delete_view,
        name='community_page_delete_note'
    ),

    # Comments
    path(
        'edit/community/<slug:community_id>/<slug:note_id>/<slug:comment_id>/',
        CommunityPageEditPostView.as_view(),
        name='community_page_edit_comment',
    ),
    path(
        'delete/community/<slug:community_id>/<slug:note_id>/<slug:comment_id>/',
        delete_view,
        name='community_page_delete_comment',
    ),

    # Replies
    path(
        'edit/community/<slug:community_id>/<slug:note_id>/<slug:comment_id>/<slug:reply_id>/',
        CommunityPageEditPostView.as_view(),
        name='community_page_edit_reply',
    ),
    path(
        'delete/community/<slug:community_id>/<slug:note_id>/<slug:comment_id>/<slug:reply_id>/',
        delete_view,
        name='community_page_delete_reply',
    ),
]