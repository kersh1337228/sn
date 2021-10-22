from django.urls import path
from user.views import UserPageView, UserAuthenticationView, \
    UserRegisterView, UserSettingsView, UserPasswordChangeView, \
    UserMainDataEditView, UserBasicPersonalDataEditView, \
    UserContactDataEditView, UserInterestsEditView, \
    UserEducationAndSpecializationEditView, UserDataVisibilityEditView


urlpatterns = [
    path(
        'user/<slug:user_id>/',
        UserPageView.as_view(),
        name='user_page'
    ),
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