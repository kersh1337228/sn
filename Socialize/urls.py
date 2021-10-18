"""Socialize URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('user.urls'), name='user'),
    path('feed/', include('user_note.urls'), name='user_note'),
    path('media/', include('user_media.urls'), name='user_media'),
    path('friends/', include('user_friend.urls'), name='user_friend'),
    path('chats/', include('user_chat.urls'), name='user_chat'),
    path('communities/', include('user_community.urls'), name='user_community'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
