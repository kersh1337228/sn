from django.urls import path
from user.views import UserPageView, UserAuthenticationView, \
    UserRegisterView, UserSettingsView, UserPasswordChangeView, \
    UserMainDataEditView, UserBasicPersonalDataEditView, \
    UserContactDataEditView, UserInterestsEditView, \
    UserEducationAndSpecializationEditView, UserDataVisibilityEditView, like_view, delete_view, UserPageEditPostView, \
    UserProfilePictureEditView

urlpatterns = [
    # User page
    path(
        'user/<slug:user_id>/',
        UserPageView.as_view(),
        name='user_page'
    ),

    # Like
    # Notes
    path(
        'like/user/<slug:user_id>/<slug:note_id>/<slug:action>/',
        like_view,
        name='like_note',
    ),

    # Comments
    path(
        'like/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/<slug:action>/',
        like_view,
        name='like_comment',
    ),

    # Replies
    path(
        'like/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/<slug:reply_id>/<slug:action>/',
        like_view,
        name='like_reply',
    ),


    # Edit and delete
    # Notes
    path(
        'edit/user/<slug:user_id>/<slug:note_id>/',
        UserPageEditPostView.as_view(),
        name='user_page_edit_note'
    ),
    path(
        'delete/user/<slug:user_id>/<slug:note_id>/',
        delete_view,
        name='user_page_delete_note'
    ),

    # Comments
    path(
        'edit/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/',
        UserPageEditPostView.as_view(),
        name='user_page_edit_comment',
    ),
    path(
        'delete/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/',
        delete_view,
        name='user_page_delete_comment',
    ),

    # Replies
    path(
        'edit/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/<slug:reply_id>/',
        UserPageEditPostView.as_view(),
        name='user_page_edit_reply',
    ),
    path(
        'delete/user/<slug:user_id>/<slug:note_id>/<slug:comment_id>/<slug:reply_id>/',
        delete_view,
        name='user_page_delete_reply',
    ),


    # Authentication urls
    path(
        'signin/',
        UserAuthenticationView.as_view(),
        name='sign_in'
    ),
    path(
        'signup/',
        UserRegisterView.as_view(),
        name='sign_up'
    ),


    # Settings urls
    path(
        'settings/profile_picture/',
        UserProfilePictureEditView.as_view(),
        name='change_user_profile_picture'
    ),
    path(
        'settings/',
        UserSettingsView.as_view(),
        name='user_settings'
    ),
    path(
        'settings/password/',
        UserPasswordChangeView.as_view(),
        name='user_password_change'
    ),
    path(
        'settings/main_data/',
        UserMainDataEditView.as_view(),
        name='user_main_data_change',
    ),
    path(
        'settings/basic_data/',
        UserBasicPersonalDataEditView.as_view(),
        name='user_basic_data_change',
    ),
    path(
        'settings/contact_data/',
        UserContactDataEditView.as_view(),
        name='user_contact_data_change',
    ),
    path(
        'settings/interests/',
        UserInterestsEditView.as_view(),
        name='user_interests_change',
    ),
    path(
        'settings/education/',
        UserEducationAndSpecializationEditView.as_view(),
        name='user_education_change',
    ),
    path(
        'settings/data_visibility/',
        UserDataVisibilityEditView.as_view(),
        name='user_data_visibility_change',
    ),
]