from django.urls import path
from user_note.views import NoteListView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
]