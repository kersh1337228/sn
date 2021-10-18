from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import CreateView, ListView
from user_community.models import Community
from user_note.forms import NoteAddForm
from user_note.models import Note


User = get_user_model()


'''
Shows all notes of users and communities,
which current user is subscribed to.
'''
class NoteListView(ListView):
    model = Note
    template_name = 'feed.html'
    context_object_name = 'notes'

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



'''
Note adding view on 
behalf of community
'''
class CommunityNoteAddView(CreateView):
    form_class = NoteAddForm
    template_name = 'community_page.html'
    slug_url_kwarg = 'community_id'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.community = Community.objects.get(community_id=self.kwargs.get('community_id'))
        return super(CommunityNoteAddView, self).form_valid(form)
