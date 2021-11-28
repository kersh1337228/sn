from django.urls import path

from user.views import NoteAPIView
from user_note.views import NoteListView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
# Edit and delete
    # Notes
    path(
        'create/',
        NoteAPIView.as_view(),
        name='create_note'
    ),
    # path(
    #     '<slug:user_id>/edit/<slug:note_id>/',
    #     UserPageEditPostView.as_view(),
    #     name='user_page_edit_note'
    # ),
    # path(
    #     '<slug:user_id>/delete/<slug:note_id>/',
    #     delete_view,
    #     name='user_page_delete_note'
    # ),
    # # Comments
    # path(
    #     '<slug:user_id>/<slug:note_id>/edit/<slug:comment_id>/',
    #     UserPageEditPostView.as_view(),
    #     name='user_page_edit_comment',
    # ),
    # path(
    #     '<slug:user_id>/<slug:note_id>/delete/<slug:comment_id>/',
    #     delete_view,
    #     name='user_page_delete_comment',
    # ),
    # # Replies
    # path(
    #     '<slug:user_id>/<slug:note_id>/<slug:comment_id>/edit/<slug:reply_id>/',
    #     UserPageEditPostView.as_view(),
    #     name='user_page_edit_reply',
    # ),
    # path(
    #     '<slug:user_id>/<slug:note_id>/<slug:comment_id>/delete/<slug:reply_id>/',
    #     delete_view,
    #     name='user_page_delete_reply',
    # ),
]