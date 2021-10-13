from django.urls import path
from user.views import UserPageView, UserAuthenticationView, UserRegisterView

urlpatterns = [
    path('user/<slug:user_id>/', UserPageView.as_view(), name='user_page'),
    path('signin/', UserAuthenticationView.as_view(), name='sign_in'),
    path('signup/', UserRegisterView.as_view(), name='sign_up'),
]