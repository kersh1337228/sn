import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, FormView
from user.views import functionally_based_view_decorator
from user_community.forms import CommunityCreateForm, CommunityEditForm
from user_community.models import Community, CommunitySubscriber, CommunitySubscribeRequest
from user_community.utils import get_community_state
from user_note.forms import PostAddForm
from user_note.models import Comment, Reply, Note


User = get_user_model()


'''Separate community page view'''
class CommunityPageView(LoginRequiredMixin, DetailView, FormView):
    model = Community
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    form_class = PostAddForm
    template_name = 'community_page.html'

    def get_success_url(self):
        return reverse_lazy(
            'community_page',
            kwargs={
                'community_id': self.kwargs.get('community_id')
            }
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )

    def get_context_data(self, **kwargs):
        community = get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )
        context = super().get_context_data(**kwargs)
        context['title'] = community.name
        context['notes'] = community.notes.all() | community.reposts.all()
        context['community_state'] = get_community_state(
            self.request.user,
            community,
        )
        return context

    def form_valid(self, form):
        if get_community_state(self.request.user, self.get_object()) == 'staff_community_page':
            owner = self.get_object()
            owner_type = 'community'
        else:
            owner = self.request.user
            owner_type = 'user'
        if 'note_btn' in self.request.POST:
            form.save(
                owner=owner,
                owner_type=owner_type,
                object_model=Note,
                type='note',
                parent=self.get_object()
            )
        elif 'comment_btn' in self.request.POST:
            note_id = [key for key in self.request.POST if '_note_' in key][0]
            form.save(
                owner=owner,
                owner_type=owner_type,
                object_model=Comment,
                type='comment',
                parent=get_object_or_404(Note, note_id=note_id)
            )
        elif 'reply_btn' in self.request.POST:
            comment_id = [key for key in self.request.POST if '_comment_' in key][0]
            form.save(
                owner=owner,
                owner_type=owner_type,
                object_model=Reply,
                type='reply',
                parent=get_object_or_404(Comment, comment_id=comment_id)
            )
        return super(CommunityPageView, self).form_valid(form)


class CommunityPageEditPostView(CommunityPageView):
    def get_template_names(self):
        if self.kwargs.get('reply_id'):
            return 'community_page_edit_reply.html'
        elif self.kwargs.get('comment_id'):
            return 'community_page_edit_comment.html'
        elif self.kwargs.get('note_id'):
            return 'community_page_edit_note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('reply_id'):
            context['current_reply_id'] = self.kwargs.get('reply_id')
        if self.kwargs.get('comment_id'):
            context['current_comment_id'] = self.kwargs.get('comment_id')
        if self.kwargs.get('note_id'):
            context['current_note_id'] = self.kwargs.get('note_id')
        return context

    def get_initial(self):
        if self.kwargs.get('reply_id'):
            self.type = 'reply'
            self.type_model = Reply
        elif self.kwargs.get('comment_id'):
            self.type = 'comment'
            self.type_model = Comment
        elif self.kwargs.get('note_id'):
            self.type = 'note'
            self.type_model = Note
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                self.type_model.objects.get(
                    **{f'{self.type}_id': self.kwargs.get(f'{self.type}_id')}
                )
            )
        )
        return initial

    def form_valid(self, form):
        self.type_model.objects.filter(
            **{f'{self.type}_id': self.kwargs.get(f'{self.type}_id')}
        ).update(
            text=form.cleaned_data.get('text'),
            update_time=datetime.datetime.now()
        )
        return HttpResponseRedirect(self.get_success_url())


'''View on which the filtered list of communities is shown'''
class CommunityListView(LoginRequiredMixin, ListView):
    model = Community
    template_name = 'community_list.html'
    context_object_name = 'communities'

    def get_queryset(self):
        return self.request.user.community_subscribes.all()


'''View of community creation page'''
class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    template_name = 'community_create.html'
    form_class = CommunityCreateForm

    def get_form(self, form_class=None):
        form = super(CommunityCreateView, self).get_form(form_class)
        form.fields['staff_list'].queryset = self.request.user.friends.all()
        return form

    def form_valid(self, form):
        form.save()
        community = get_object_or_404(
            Community,
            community_id=Community.objects.get(
                name=form.cleaned_data.get('name')
            ).community_id
        )
        community.staff_list.add(self.request.user)
        return redirect(
            'community_page',
            community_id=community.community_id
        )

    def get_success_url(self):
        return reverse_lazy(
        'community_page',
        kwargs={
            'community_id': self.kwargs['community_id'],
        }
    )


'''
View to edit the community settings, 
only community staff can do so
'''
class CommunityEditView(LoginRequiredMixin, UpdateView):
    model = Community
    template_name = 'community_edit.html'
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    form_class = CommunityEditForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )

    def get_success_url(self):
        return reverse_lazy(
        'community_page',
        kwargs={
            'community_id': self.kwargs['community_id'],
        }
    )


'''
View to delete the community,
only community staff can do so
'''
class CommunityDeleteView(LoginRequiredMixin, DeleteView):
    model = Community
    template_name = 'community_delete.html'
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    success_url = reverse_lazy('community_list')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )


'''View of sending subscribe request to private community'''
@login_required
@functionally_based_view_decorator
def subscribe_view(request, community_id):
    community = get_object_or_404(Community, community_id=community_id)
    if community.is_public:
        subscriber = CommunitySubscriber(
            from_user=request.user,
            to_community=community,
        )
        subscriber.save()
        request.user.community_subscribes.add(community)
    else:
        subscribe_request = CommunitySubscribeRequest(
            from_user=request.user,
            to_community=community,
            state=None,
        )
        subscribe_request.save()
        community.subscribe_requests.add(subscribe_request)
    return redirect('community_page', community_id)


@login_required
def unsubscribe_view(request, community_id):
    if request.user.is_active:
       try:
           request.user.community_subscribes.get(community_id=community_id).delete()
           CommunitySubscriber.objects.get(from_user=request.user).delete()
       except:
           pass
       return redirect('community_page', community_id)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)

'''View of answering on subscribe request'''
@login_required
def subscribe_request_result(request, user_id, community_id, result):
    if request.user.is_active:
        request_user = get_object_or_404(User, user_id=user_id)
        community = get_object_or_404(Community, community_id=community_id)
        if result == 'accept':
            subscriber = CommunitySubscriber(
                from_user=request_user,
                to_community=community,
            )
            subscriber.save()
            request_user.community_subscribes.add(community)
        community.subscribe_requests.get(from_user=request_user).delete()
        return redirect('subscribe_requests')
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)
