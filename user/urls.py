from django.urls import path
from user.views import UserPageView, UserAuthenticationView, \
    UserRegisterView, UserSettingsView, UserPasswordChangeView, \
    UserMainDataEditView, UserBasicPersonalDataEditView, \
    UserContactDataEditView, UserInterestsEditView, \
    UserEducationAndSpecializationEditView, UserDataVisibilityEditView, like_view, delete_view, UserPageEditPostView, \
    UserProfilePictureEditView, NoteAPIView

urlpatterns = [
    # User page
    path(
        '<slug:user_id>/',
        UserPageView.as_view(),
        name='user_page'
    ),
    # Like
    path(
        'post/<slug:action>/',
        like_view,
        name='like_post',
    ),
    # Authentication urls
    path(
        'auth/signin/',
        UserAuthenticationView.as_view(),
        name='sign_in'
    ),
    path(
        'auth/signup/',
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
        'settings/list/',
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