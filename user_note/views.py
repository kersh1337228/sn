from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from user_community.models import Community
from user_note.forms import PostAddForm
from user_note.models import Note, Comment, Reply

User = get_user_model()


'''
Shows all notes of users and communities,
which current user is subscribed to.
'''
class NoteListView(ListView, FormView):
    model = Note
    template_name = 'feed.html'
    context_object_name = 'notes'
    form_class = PostAddForm

    def get_success_url(self):
        return reverse_lazy('note_list')

    def get_queryset(self):
        queryset = Note.objects.filter(
            Q(user__in=self.request.user.user_subscribes.all()) |
            Q(community__in=self.request.user.community_subscribes.all())
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Feed'
        return context

    def form_valid(self, form):
        if 'note_btn' in self.request.POST:
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Note,
                type='note',
                parent=self.request.user
            )
        elif 'comment_btn' in self.request.POST:
            note_id = [key for key in self.request.POST if '_note_' in key][0]
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Comment,
                type='comment',
                parent=get_object_or_404(Note, note_id=note_id)
            )
        elif 'reply_btn' in self.request.POST:
            comment_id = [key for key in self.request.POST if '_comment_' in key][0]
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Reply,
                type='reply',
                parent=get_object_or_404(Comment, comment_id=comment_id)
            )
        return super(NoteListView, self).form_valid(form)


'''
Note adding view on 
behalf of community
'''
class CommunityNoteAddView(CreateView):
    form_class = PostAddForm
    template_name = 'community_page.html'
    slug_url_kwarg = 'community_id'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.community = Community.objects.get(community_id=self.kwargs.get('community_id'))
        return super(CommunityNoteAddView, self).form_valid(form)
